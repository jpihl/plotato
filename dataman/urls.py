from django.conf.urls.defaults import patterns, url
from djangorestframework.views import ListOrCreateModelView, InstanceModelView
from dataman.resources import DataSetResource, DataResource


urlpatterns = patterns('',
    url(r'^$', ListOrCreateModelView.as_view(resource=DataSetResource), name='datasets-root'),
    url(r'^(?P<key>[^/]+)/$', InstanceModelView.as_view(resource=DataSetResource), name='dataset'),
    url(r'^(?P<dataset>[^/]+)/dataentries/$', ListOrCreateModelView.as_view(resource=DataResource), name='dataentries'),
    url(r'^(?P<dataset>[^/]+)/dataentries/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=DataResource)),
    
    url(r'^create/$', 'create'),
    url(r'^edit/(?P<dataset_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$',   'edit'),
    url(r'^delete/(?P<dataset_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'delete'),
    url(r'^details/(?P<dataset_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/$', 'details'),
    url(r'^delete_entry/(?P<entry_id>[^/]+)', 'delete_entry'),
)
