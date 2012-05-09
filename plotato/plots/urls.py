from django.conf.urls.defaults import patterns, url, include




urlpatterns = patterns('plotato.plots',
	url(r'^(?P<plot_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$'                , 'views.show'),
    url(r'^(?P<plot_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/(?P<x_val>\d+)x(?P<y_val>\d+)/$', 'views.show'),
    url(r'^create/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'       , 'views.create'),
    url(r'^edit/(?P<plot_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'            , 'views.edit'),
    url(r'^delete/(?P<plot_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'          , 'views.delete'),
    url(r'^details/(?P<plot_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$'         , 'views.details'))