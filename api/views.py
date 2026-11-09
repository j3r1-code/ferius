from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Класс, который отключает проверку CSRF для DRF
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Ничего не проверяем, пропускаем запрос

# Авторизация
class PureApiLoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                "status": "success",
                "message": "Успешная авторизация!",
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "message": "Неверный логин или пароль"
            }, status=status.HTTP_400_BAD_REQUEST)

# Регистрация
class RegisterView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email', '')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Заполните все обязательные поля"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"message": "Пользователь с таким именем уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)

        return Response({
            "status": "success",
            "message": "Регистрация прошла успешно!",
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

# Профиль
class UserProfileView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "username": request.user.username,
                "email": request.user.email,
                "date_joined": request.user.date_joined.strftime("%Y-%m-%d")
            })
        return Response({"message": "Не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

# Выход
class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def post(self, request):
        logout(request)
        return Response({"message": "Успешный выход из системы"})