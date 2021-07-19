from celery import shared_task
from django.db.models import Q, QuerySet

from server.apps.notifications.logic.classes import BaseNotificationUseCase
from server.apps.notifications.models import Notification
from server.apps.users.models import User


@shared_task
def send_notifications():
    users: QuerySet[User] = User.objects.all()
    notifications: QuerySet[Notification] = Notification.objects.filter(Q(email_send=False) | Q(push_send=False))
    BaseNotificationUseCase(notifications, users)()


@shared_task
def clear_notifications():
    Notification.objects.filter(
        email_send=True,
        push_send=True,
    ).delete()
