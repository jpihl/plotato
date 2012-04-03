from django.conf.urls.defaults import patterns, url, include
from tastypie.api import Api
from projects.api import UserResource, ProjectResource, TestResource, RunResource

rest_api = Api(api_name='v1')
rest_api.register(TestResource())
rest_api.register(UserResource())
rest_api.register(ProjectResource())
rest_api.register(RunResource())

urlpatterns = patterns('projects',
	url(r'^$',                                                                                            'views.home'),
    url(r'^about/$',                                                                                      'views.about'),
    url(r'^project/create$',                                                                              'views.create_project'),
    url(r'^project/edit/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',   'views.edit_project'),
    url(r'^project/details/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$','views.details_project'),
    url(r'^project/delete/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$', 'views.delete_project'),
    url(r'^test/create/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',    'views.create_test'),
    url(r'^test/edit/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',         'views.edit_test'),
    url(r'^test/details/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',      'views.details_test'),
    url(r'^test/delete/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',       'views.details_test'),
   # url(r'^test/run/create/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',        'views.create_run'),
   # url(r'^run/edit/(?P<run_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',                'views.edit_run'),
   # url(r'^run/details/(?P<run_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',             'views.details_run'),
)

urlpatterns += patterns('',
    # URLs for adding results
    # (r'^result/add/json/$', 'add_json_results'),
    # (r'^result/add/$', 'add_result'),
    (r'^api/', include(rest_api.urls)),
)