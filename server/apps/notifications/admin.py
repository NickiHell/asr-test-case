from django.contrib import admin

from server.apps.notifications.models import Notification


@admin.register(Notification)
class _(admin.ModelAdmin):
    list_display = ('id', 'email_send', 'push_send', 'message')
    list_filter = ('email_send', 'push_send')
