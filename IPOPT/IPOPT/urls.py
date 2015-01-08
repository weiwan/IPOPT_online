from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
# import accounts.urls
import submission.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IPOPT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^mongonaut/', include('mongonaut.urls')),
    url(r'^$', 'submission.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/$', 'accounts.views.login'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^discuss/', include('discussion.urls')),
    url(r'^analysis/', include('analysis.urls')),
    url(r'^notification/', include('notification.urls')),

    url(r'^', include(submission.urls)),
    url(r'^500/$', TemplateView.as_view(template_name="500.html")),
    url(r'^404/$', TemplateView.as_view(template_name="404.html")),
    url(r'^403/$', TemplateView.as_view(template_name="403.html")),
)
