from django.conf.urls import patterns, include, url, static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from invdb import views
from django.contrib import admin

admin.autodiscover()
#handler404 = views.handler404

urlpatterns = patterns('',
                       url(r'^$', include('invdb.urls')),
                       url('^', include('authenticator.urls')),
                       url('^invdb/', include('invdb.urls')),
 #   url('^importer/', include('importer.urls')),
 #   url('^kickstart/', include('kickstart.urls')),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()

