from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IPOPT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'notification.views.list', name='notification_list'),
    url(r'^markallread/$', 'notification.views.markallread', name='markallread'),
    url(r'^(?P<notification_id>\w+)/$', 'notification.views.get_notification_url', name='get_notification_url'),
)
