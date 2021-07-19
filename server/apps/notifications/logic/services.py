from abc import ABC, abstractmethod

from django.db.models import QuerySet

from server.apps.notifications.models import Notification
from server.apps.users.models import User


class AbstractNotificationService(ABC):
    """Абстрактный сервис уведомлений"""

    @staticmethod
    @abstractmethod
    def invoke(notification: Notification, user: User = None):
        pass


class PushNotificationService(AbstractNotificationService):

    @staticmethod
    def invoke(notification: Notification, user: User = None) -> None:
        if not notification.push_send:
            notification.push_send = True
            notification.save()


class EmailNotificationService(AbstractNotificationService):

    @staticmethod
    def invoke(notification: Notification, user: User = None) -> None:
        if not notification.email_send:
            notification.email_send = True
            notification.save()