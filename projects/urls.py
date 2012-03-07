from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('projects',
    url(r'^$',                                  'views.index'),
    url(r'^create/$',                           'views.create'),
    url(r'^edit/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',   'views.edit'),
    url(r'^delete/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'views.delete'),
    url(r'^details/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'views.details'),
    url(r'^plots/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/', include('projects.plots.urls')),
)