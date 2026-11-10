from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Отправитель")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Получатель")
    subject = models.CharField(max_length=255, verbose_name="Тема")
    body = models.TextField(verbose_name="Текст сообщения")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        ordering = ['-created_at'] # Свежие сообщения будут сверху

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.subject}"


class UserProfile(models.Model):
  user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name='profile'
  )
  failed_attempts = models.IntegerField(default=0)

  def __str__(self):
    return f'Профиль {self.user.username}'

#орм
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)
    