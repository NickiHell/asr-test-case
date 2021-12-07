from django.db import models

from server.apps.core.mixins import DateTimeMixin
from server.apps.users.models import User


class Notification(DateTimeMixin, models.Model):
    """Уведомления для пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',
                             verbose_name='Пользователь',
                             null=True, blank=True, db_index=True)
    email_send = models.BooleanField('Email отправлен', default=False)
    push_send = models.BooleanField('Push отправлен', default=False)
    message = models.TextField(null=True, blank=True)

    class Meta(object):
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        indexes = (
            models.Index(fields=['created_at', 'updated_at']),
            models.Index(fields=['user', 'email_send', 'push_send']),
        )
