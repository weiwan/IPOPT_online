from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'IPOPT.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^$', include('accounts.urls')),

	url(r'^list/$', 'discussion.views.discuss', name='discuss'),
	url(r'^create/$', 'discussion.views.createDiscuss', name='create_discuss'),
	url(r'^create/(?P<resultID>\w+)/$', 'discussion.views.createDiscuss', name='create_discuss'),
	url(r'^mine/$', 'discussion.views.myDiscuss', name='my_discuss'),
	url(r'^search/$', 'discussion.views.search', name='search'),
	url(r'^detail/(?P<discussionID>\w+)/$', 'discussion.views.discuss_detail', name='discuss_detail'),
	url(r'^comment/(?P<discussionID>\w+)/$', 'discussion.views.postComment', name='post_comment'),
	url(r'^dislike/(?P<discussionID>\w+)/$', 'discussion.views.dislike', name='dislike'),
	url(r'^like/(?P<discussionID>\w+)/$', 'discussion.views.like', name='like'),
	url(r'^findtag/(?P<tagtext>\w+)/$', 'discussion.views.findDiscuss', name='findDiscuss'),
)
