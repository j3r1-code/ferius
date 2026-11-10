# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    recipient_to_send = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Message
        fields = ['id', 'sender_username', 'recipient_username', 'recipient_to_send', 'subject', 'body', 'is_read', 'created_at']
        read_only_fields = ['id', 'is_read', 'created_at']

    def validate_recipient_to_send(self, value):
        try:
            return User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким именем не найден.")

    # <-- ДОБАВЬ ИЛИ ОБНОВИ ЭТОТ МЕТОД НИЖЕ -->
    def create(self, validated_data):
        # Удаляем временное поле из данных, чтобы оно не шло в базу напрямую
        recipient_user = validated_data.pop('recipient_to_send')
        
        # Создаем объект с правильным полем 'recipient'
        return Message.objects.create(recipient=recipient_user, **validated_data)
