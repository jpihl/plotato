from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plotato.views.home', name='home'),


    # (r'^', include('plotato_nosql.projects.urls')),
    (r'^plot/', include('plotato_nosql.plots.urls')),
       (r'^', include('plotato_nosql.projects.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # needed for development server
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()