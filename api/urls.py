from django.urls import path
from .views import PureApiLoginView, RegisterView, UserProfileView, LogoutView

urlpatterns = [
    path('login/', PureApiLoginView.as_view(), name='api_login'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('profile/', UserProfileView.as_view(), name='api_profile'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
]