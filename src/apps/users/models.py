from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.mixins import DateTimeMixin, UUIDMixin


class User(UUIDMixin, DateTimeMixin, AbstractUser):
    """Пользователь"""
    first_name = models.CharField('Имя', max_length=256)
    last_name = models.CharField('Фамилия', max_length=256)
    timezone = models.DateTimeField('Тймзона')
    email = models.EmailField()

    class Meta:
        verbose_name = 'Пользоатель'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]
