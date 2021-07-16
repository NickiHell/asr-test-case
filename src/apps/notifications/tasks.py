import uuid

from apps.core.celery import app
from apps.notifications.models import Notification
from apps.users.models import User


@app.task
def send_notification_to_user(notification_id: uuid) -> None:
    users_emails = User.objects.values_list('email')
    message = Notification.objects.get(id=notification_id).payload

