from django.urls import include, path

v1_urlpatterns = [
    path('notifications/', include('apps.notifications.api.v1.urls', namespace='notifications.v1')),
    path('users/', include('apps.users.api.v1.urls', namespace='users.v1')),
]
