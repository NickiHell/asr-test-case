from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.mixins import DateTimeMixin, UUIDMixin


class User(UUIDMixin, DateTimeMixin, AbstractUser):
    """Пользователь"""
    usertime = models.DateTimeField('Время пользователя', null=True, blank=True)
    email = models.EmailField('Эмейл', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользоатель'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]
