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
	(r'^findost/results$', 'findost.views.results'),
	(r'^findost/(?P<kind>[a-z]+)$', 'findost.views.search'),
	(r'^findost/show/details/(?P<id>\d+)$','findost.views.showdetails'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)$','findost.views.details'),
	(r'^findost/show/details/(?P<id>\d+)/episodes$','findost.views.loadepisodes'),
	(r'^login$','findost.views.log_in'),
	(r'^subscribe$','findost.views.subscribe'),
	(r'^showlogin$','findost.views.showlogin'),
	(r'^showsubscribe$','findost.views.showsubscribe'),
	(r'^logout$','findost.views.log_out'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)/edit$','findost.views.edit'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)/comment$','findost.views.comment'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)/cancel$','findost.views.cancel'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)/save$','findost.views.savechanges'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<gid>\d+)/(?P<id>\d+)/checktrack$','findost.views.checktrack'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)/report/(?P<sid>\d+)$','findost.views.report'),
	(r'^findost/(?P<kind>[a-z]+)/details/(?P<id>\d+)/unreport/(?P<sid>\d+)$','findost.views.unreport'),
)
