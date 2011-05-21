from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ost.views.home', name='home'),
    # url(r'^ost/', include('ost.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

	(r'^home$', 'findost.views.home'),
	(r'^findost/(?P<kind>[a-z]+)$', 'findost.views.search'),
	(r'^findost/(?P<kind>[a-z]+)/results$', 'findost.views.results'),
	(r'^findost/show/details/(?P<id>\d+)$','findost.views.showdetails'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)$','findost.views.details'),
	(r'^findost/show/details/(?P<id>\d+)/episodes$','findost.views.loadepisodes'),
	(r'^login$','findost.views.login'),
	(r'^subscribe$','findost.views.subscribe'),
)