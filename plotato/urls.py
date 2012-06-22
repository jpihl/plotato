from django.conf import settings
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    (r'^', include('plotato.projects.urls')),
)

if settings.DEBUG:
    # needed for development server
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()