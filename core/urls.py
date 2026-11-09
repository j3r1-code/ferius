from api.views import CustomAuthToken
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', CustomAuthToken.as_view()),
]


from django.contrib import admin
from django.urls import path, include
from api.views import CustomLoginView, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',profile_view, name = 'profile'),
    path('login/', CustomLoginView.as_view(), name='login'), # Прямой путь /login/
    path('api/', include('api.urls')),
]
