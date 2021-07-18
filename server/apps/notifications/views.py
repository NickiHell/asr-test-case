from typing import List, Tuple

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from server.apps.notifications.forms import NotificationForm
from server.apps.notifications.models import Notification
from server.apps.users.models import User


class NotificationSendView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'html/index.html', {'form': NotificationForm})

    @staticmethod
    def post(request, *args, **kwargs):
        users: QuerySet[User] = User.objects.all()
        form = NotificationForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            notifications: Tuple[Notification] = tuple(
                Notification(
                    user=x,
                    message=form.data['message']
                ) for x in users
            )
            Notification.objects.bulk_create(notifications)
            return HttpResponse('OK')
        return HttpResponse('Not OK')
