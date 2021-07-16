import uuid

from apps.core.taskapp.celery import app


@app.task
def send_notification_in_queue(notification_id: uuid) -> None:
    pass
