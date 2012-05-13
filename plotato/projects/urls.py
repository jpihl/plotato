from django.conf.urls.defaults import patterns, url, include
from tastypie.api import Api
from api import ProjectResource, TestResource, RunResource

rest_api = Api(api_name='v1')
rest_api.register(TestResource())
rest_api.register(ProjectResource())
rest_api.register(RunResource())

urlpatterns = patterns('plotato.projects',
	url(r'^$',                                                                                            'views.home'),
    url(r'^about$',                                                                                       'views.about'),

    url(r'^user/login$',                                                                                  'views.log_in'),
    url(r'^user/logout$',                                                                                 'views.log_out'),
    url(r'^user/create/$',                                                                                'views.create_user'),
    url(r'^user/edit/$',                                                                                  'views.edit_user'),
    url(r'^user/details/$',                                                                               'views.details_user'),
    url(r'^user/delete/$',                                                                                'views.delete_user'),

    url(r'^project/create/$',                                                                              'views.create_project'),
    url(r'^project/edit/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',   'views.edit_project'),
    url(r'^project/details/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$','views.details_project'),
    url(r'^project/delete/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$', 'views.delete_project'),

    url(r'^test/create/(?P<project_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',    'views.create_test'),
    url(r'^test/edit/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',         'views.edit_test'),
    url(r'^test/details/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',      'views.details_test'),
    url(r'^test/delete/(?P<test_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',       'views.delete_test'),
    url(r'^run/delete/(?P<run_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$',         'views.delete_run'),
)

urlpatterns += patterns('',
    (r'^api/', include(rest_api.urls)),
)