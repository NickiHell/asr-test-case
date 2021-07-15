from django.db import models

from apps.core.mixins import DateTimeMixin, UUIDMixin
from apps.user.models import User


class Notification(UUIDMixin, DateTimeMixin, models.Model):
    """Уведомления для пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Пользователь')
    email_send = models.BooleanField('Email отправлен', default=False)
    push_send = models.BooleanField('Push отправлен', default=False)
    payload = models.TextField()

    class Meta(object):
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        indexes = (
            models.Index(fields=['created_at', 'updated_at']),
            models.Index(fields=['user', 'email_send', 'push_send']),
        )
