from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication
from .models import Message
from .serializers import MessageSerializer


# Отключение проверки CSRF для безопасной работы сессий в Docker + Nginx
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Пропускаем проверку CSRF-токена


class PureApiLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"message": "Введіть логін та пароль"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user) # Генерирует сессионную куку в браузере
            
            email_str = user.email if user.email else "не указан"
            date_joined_str = user.date_joined.strftime("%Y-%m-%d") if user.date_joined else ""
            
            return Response({
                "status": "success",
                "message": "Успешная авторизация!",
                "user": {
                    "username": user.username,
                    "email": email_str,
                    "date_joined": date_joined_str
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "message": "Неверный логин или пароль"
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email', '')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Имя пользователя и пароль обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"message": "Пользователь с таким именем уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)

        return Response({
            "status": "success",
            "message": "Пользователь успешно зарегистрирован!",
            "user": {
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined.strftime("%Y-%m-%d")
            }
        }, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        email_str = user.email if user.email else "не указан"
        return Response({
            "username": user.username,
            "email": email_str,
            "date_joined": user.date_joined.strftime("%Y-%m-%d")
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"message": "Успешный выход из системы"}, status=status.HTTP_200_OK)


# --- ПОЧТОВЫЕ ЭНДПОИНТЫ (ИСПРАВЛЕННЫЕ) ---

class MessageInboxView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    # Получить список входящих писем для текущего пользователя
    def get(self, request):
        messages = Message.objects.filter(recipient=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Отправить новое письмо
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            # Передаем только sender. Поле recipient теперь достается внутри сериализатора!
            serializer.save(sender=request.user)
            return Response({"status": "success", "message": "Сообщение успешно отправлено!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    # Посмотреть содержание конкретного письма
    def get(self, request, pk):
        try:
            message = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            return Response({"message": "Сообщение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        
        # Безопасность: читать могут только отправитель или получатель
        if message.recipient != request.user and message.sender != request.user:
            return Response({"message": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        # Если получатель открыл письмо впервые — помечаем как прочитанное
        if message.recipient == request.user and not message.is_read:
            message.is_read = True
            message.save()
            
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
