from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path
from django.views.generic import TemplateView
from health_check import urls as health_urls

from server.apps.notifications.views import NotificationSendView

admin.autodiscover()

urlpatterns = [
    # Apps:
    # path('core/', include(main_urls, namespace='core')),

    # Health checks:
    path('health/', include(health_urls)),  # noqa: DJ05

    # django-admin:
    path('admin/doc/', include(admindocs_urls)),  # noqa: DJ05
    path('admin/', admin.site.urls),

    # Text and xml media files:
    path('robots.txt', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    path('humans.txt', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),

    # It is a good practice to have explicit index view:
    path('', NotificationSendView.as_view(), name='index'),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
                  ] + urlpatterns + static(  # type: ignore
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
