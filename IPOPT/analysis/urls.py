from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IPOPT.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^data/pie/$', 'analysis.views.getData1', name="data_pie"),
    url(r'^data/loglog/$', 'analysis.views.getData2', name="data_loglog"),
	url(r'^data/statckbar/$', 'analysis.views.getData3', name="data_stackbar"),
	url(r'^plot/pie/$', 'analysis.views.displayData1'),
	url(r'^plot/loglog/$', 'analysis.views.displayData2'),
	url(r'^plot/stackbar/$', 'analysis.views.displayData3'),
	url(r'^$', 'analysis.views.displayAll', name="analysis")
)