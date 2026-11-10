from django.urls import path
from .views import PureApiLoginView, RegisterView, UserProfileView, LogoutView
# api/urls.py
from django.urls import path
from .views import (
    RegisterView, 
    PureApiLoginView, 
    UserProfileView, 
    LogoutView, 
    MessageInboxView,  # <-- Добавь импорт
    MessageDetailView   # <-- Добавь импорт
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', PureApiLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Новые маршруты для писем
    path('messages/', MessageInboxView.as_view(), name='messages-inbox'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]

