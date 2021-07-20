from abc import ABC, abstractmethod
from typing import Tuple, Union, Type

from django.db.models import F, QuerySet, Q
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
    def invoke_service(self, service, data):
        pass

    def __call__(self, *args, **kwargs):
        return self.execute()


class BaseNotificationUseCase(AbstractNotificationUseCase):
    """Базовый класс для отправки уведомлений пользователям"""
    PushService = PushNotificationService
    EmailService = EmailNotificationService
    UsersForPush: Union[QuerySet[User], None] = None
    UsersForEmail: Union[QuerySet[User], None] = None

    def execute(self):
        self.UsersForPush, self.UsersForEmail = self._get_querysets()
        self.invoke_service(self.PushService, self.UsersForPush)
        self.invoke_service(self.EmailService, self.UsersForEmail)

    def invoke_service(self,
                       service: Type[Union[PushNotificationService, EmailNotificationService]],
                       data: QuerySet[User]):
        notifications = self._notifications.filter(user_id__in=data)
        for notification in notifications:
            service.invoke(notification, None)

    def _get_querysets(self) -> Tuple[QuerySet[User], QuerySet[User]]:
        now = timezone.now()
        users_for_push = self._users.annotate(
            usertime=Cast(now + F('user_timedelta'), output_field=DateTimeField())
        ).filter(
            Q(usertime__hour__range=[now.replace(hour=10).hour, now.replace(hour=21).hour]),
        )

        return users_for_push, self._users
