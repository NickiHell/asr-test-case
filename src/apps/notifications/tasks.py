import uuid

from apps.core.celery import app


@app.task
def send_notification_to_user(notification_id: uuid) -> None:
    pass
