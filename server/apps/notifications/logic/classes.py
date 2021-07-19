from abc import ABC, abstractmethod
from typing import Tuple

from django.db.models import QuerySet, F
from django.db.models.fields import DateTimeField
from django.db.models.functions import Cast
from django.utils import timezone

from server.apps.notifications.logic.services import (
    AbstractNotificationService,
    EmailNotificationService,
    PushNotificationService,
)
from server.apps.notifications.models import Notification
from server.apps.users.models import User


class AbstractNotificationUseCase(ABC):
    """Абстрактный класс для отправки уведомлений"""

    def __init__(self, notifications: QuerySet[Notification], users: QuerySet[User]):
        self._notifications: QuerySet[Notification] = notifications
        self._users: QuerySet[User] = users

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def invoke_service(self, service: AbstractNotificationService):
        pass

    def __call__(self, *args, **kwargs):
        return self.execute()


class BaseNotificationUseCase(AbstractNotificationUseCase):
    """Базовый класс для отправки уведомлений пользователям"""
    PushService = PushNotificationService
    EmailService = EmailNotificationService
    UsersForPush = None
    UsersForEmail = None

    def execute(self):
        self.UsersForPush, self.UsersForEmail = self._get_querysets()
        self.invoke_service(self.PushService, self.UsersForPush)
        self.invoke_service(self.EmailService, self.UsersForPush)
        self.invoke_service(self.EmailService, self.UsersForEmail)

    def invoke_service(self, service: AbstractNotificationService, data: QuerySet[User]):
        notifications = self._notifications.filter(user_id__in=data)
        for notification in notifications:
            service.invoke(notification, None)

    def _get_querysets(self) -> Tuple[QuerySet, QuerySet]:
        now = timezone.now()
        users_for_push = self._users.annotate(
            dt=Cast(now + F('user_timedelta'), output_field=DateTimeField())
        ).filter(
            dt__range=(now.replace(hour=10, minute=0), now.replace(hour=21, minute=59))
        )

        users_for_email = self._users.exclude(id__in=users_for_push)
        return users_for_push, users_for_email
