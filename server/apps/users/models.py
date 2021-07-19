from django.contrib.auth.models import AbstractUser
from django.db import models
from faker import Faker

from server.apps.core.mixins import DateTimeMixin, UUIDMixin

faker = Faker()


class User(UUIDMixin, DateTimeMixin, AbstractUser):
    """Пользователь"""
    user_timedelta = models.DurationField('Timedelta пользователя на уведомления', null=True)
    email = models.EmailField('Email', default=faker.email())

    class Meta:
        verbose_name = 'Пользоатель'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]
