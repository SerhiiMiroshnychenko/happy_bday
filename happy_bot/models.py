"""МОДЕЛЬ PROFILE"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Модель профілю користувача в телеграм боті
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
