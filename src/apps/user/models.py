from django.db import models

from apps.core.mixins import DateTimeMixin, UUIDMixin


class User(UUIDMixin, DateTimeMixin, models.Model):
    """Пользователь"""
    first_name = models.CharField('Имя', max_length=256)
    last_name = models.CharField('Фамилия', max_length=256)
    timezone = models.DateTimeField('Тймзона')  # ???
    email = models.EmailField()
    is_auth = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользоатель'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]
