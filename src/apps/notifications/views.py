from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.notifications.forms import NotificationForm
from apps.notifications.models import Notification
from apps.users.models import User


class NotificationSendView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'notifications/push_message.html', {'form': NotificationForm})

    @staticmethod
    def post(request, *args, **kwargs):
        form = NotificationForm(request.POST)
        user = User.objects.filter(first_name=form.data['user'])
        if form.is_valid() and request.user.is_staff and user:
            notification = Notification.objects.create(user=user, payload=form.data['text'])
            return HttpResponse('OK')
        return HttpResponse('Not OK')
