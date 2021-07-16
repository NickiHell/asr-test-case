from django.urls import path

from apps.notifications.views import NotificationSendView


app_name = 'notifications'

urlpatterns = [
    path('', NotificationSendView.as_view(), name='send_notification'),
]
