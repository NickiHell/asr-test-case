from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.notifications.forms import NotificationForm
from apps.notifications.models import Notification
from apps.notifications.tasks import send_notification_to_user
from apps.users.models import User


class NotificationSendView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'notifications/push_message.html', {'form': NotificationForm})

    @staticmethod
    def post(request, *args, **kwargs):
        form = NotificationForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            notification_id = str(Notification.objects.create(payload=form.data['text']).id)
            send_notification_to_user.delay(notification_id)
            return HttpResponse('OK')
        return HttpResponse('Not OK')
