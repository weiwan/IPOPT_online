from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IPOPT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'}, name='logout'),
	url(r'^register/$', 'accounts.views.register', name='register'),
	url(r'^confirm/(?P<code>[0-9A-Za-z]+)/(?P<username>.+)/$', 'accounts.views.register_confirm'),
	url(r'^activate/$', 'accounts.views.register_activate'),
	url(r'^view_profile/$', 'accounts.views.view_profile', name='view_profile'),
	url(r'^edit_profile/$', 'accounts.views.edit_profile', name='edit_profile'),
	url(r'^view_profile/(?P<user_id>[0-9A-Za-z]+)/$', 'accounts.views.view_profile'),
	url(r'^change_password/$', 'accounts.views.change_password', name='change_password'),
	url(r'^forgot_password/$', 'accounts.views.forgot_password', name='forgot_password'),
	url(r'^reset_forgotten_password/(?P<username>[a-zA-Z0-9_@\+\-.]+)/(?P<token>[a-z0-9\-]+)$', 'accounts.views.reset_forgotten_password', name='reset_forgotten_password'),
)
