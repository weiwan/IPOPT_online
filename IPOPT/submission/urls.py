from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IPOPT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^result/$', 'submission.views.result', name='result'),
    url(r'^submit/$', 'submission.views.newsubmit', name='submission'),
    url(r'^getresultfile/(?P<resultID>\w+)/$', 'submission.views.getresultfile', name='getresultfile'),
    url(r'^getsubmissionfile/(?P<submissionID>\w+)/$', 'submission.views.getsubmissionfile', name='getsubmissionfile'),
    url(r'^sendresult/(?P<resultID>\w+)/$', 'submission.views.sendresult', name='sendresult'),
    # url(r'^newsubmit/$', 'submission.views.newsubmit'),
    
)
