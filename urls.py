from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^dataman/', include('dataman.urls')),
	url(r'^', include('projects.urls')),
)