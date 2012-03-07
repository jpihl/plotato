from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('projects.plots.views',
    url(r'^(?P<plot_id>\d+)/$', 'show'),
    url(r'^create/$'		  , 'create'),
    url(r'^edit/(?P<plot_id>\d+)/$', 'edit'),
    url(r'^delete/(?P<plot_id>\d+)/$', 'delete'),
)