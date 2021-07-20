import datetime
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.utils import timezone
from faker import Faker

from server.apps.notifications.logic.classes import BaseNotificationUseCase
from server.apps.notifications.models import Notification
from server.apps.users.models import User


class TestBaseNotificationUseCase:
    _class: BaseNotificationUseCase = BaseNotificationUseCase
    _now = timezone.now()
    _faker = Faker()

    def test_execute(self):
        pass

    @pytest.mark.parametrize(
        "user_timedelta,nowtime,push_count,emails_count",
        [
            (timezone.timedelta(hours=1), datetime.datetime(2020, 1, 1, 10, 20), 10, 10),
            (timezone.timedelta(hours=1), datetime.datetime(2020, 1, 1, 22, 20), 0, 10),
            (timezone.timedelta(hours=0), datetime.datetime(2020, 1, 1, 21, 59), 10, 10),
            (timezone.timedelta(hours=6), datetime.datetime(2020, 1, 1, 9, 59), 10, 10),
        ]
    )
    def test_parametrized_pushes_and_emails(self, user_timedelta, nowtime, push_count, emails_count):
        users = User.objects.bulk_create(
            User(
                username=str(uuid4()),
                first_name=self._faker.first_name(),
                last_name=self._faker.last_name(),
                user_timedelta=user_timedelta,
            ) for _ in range(10)
        )
        notifications = Notification.objects.bulk_create(
            Notification(
                user=x,
                message=self._faker.first_name(),
            ) for x in users
        )
        users = User.objects.filter(id__in=(x.id for x in users))
        notifications = Notification.objects.filter(id__in=(x.id for x in notifications))
        with patch.object(timezone, 'now', return_value=nowtime):
            users_for_push, users_for_email = self._class(notifications, users)._get_querysets()
            assert len(users_for_email) == emails_count
            assert len(users_for_push) == push_count
