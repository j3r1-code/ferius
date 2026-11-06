from api.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):

  def post(self, request, *args, **kwargs):
    username = request.data.get('username')

    try:
      user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
      return Response(
          {'status': 'denied', 'message': 'Неверный логин'}, status=400
      )

    if not user_obj.is_active:
      return Response(
          {
              'status': 'denied',
              'message': (
                  'Аккаунт заблокирован из-за превышения числа попыток входа.'
              ),
          },
          status=403,
      )

    profile, _ = UserProfile.objects.get_or_create(user=user_obj)

    serializer = self.serializer_class(
        data=request.data, context={'request': request}
    )

    if not serializer.is_valid():
      profile.failed_attempts += 1
      profile.save()

      attempts_left = 5 - profile.failed_attempts

      if profile.failed_attempts >= 5:
        user_obj.is_active = False
        user_obj.save()
        return Response(
            {
                'status': 'denied',
                'message': (
                    'Превышено количество попыток. Аккаунт заблокирован.'
                ),
            },
            status=403,
        )

      return Response(
          {
              'status': 'denied',
              'message': (
                  f'Неверный пароль. Осталось попыток: {attempts_left}'
              ),
          },
          status=400,
      )

    profile.failed_attempts = 0
    profile.save()

    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)

    return Response({'status': 'successful', 'token': token.key}, status=200)