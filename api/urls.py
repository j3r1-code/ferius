from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from api.views import CustomLoginView
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from api.views import CustomLoginView, profile_view

class CustomLoginView(LoginView):
    template_name = 'auth_app/login.html'
    redirect_authenticated_user = True

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', profile_view, name='profile'),  # Главная страница после входа
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]