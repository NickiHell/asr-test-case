from django.urls import path

from apps.notifications.views import NotififcationSendView


app_name = 'notifications'

urlpatterns = [
    path('', NotififcationSendView.as_view(), name='send_notification'),
]

