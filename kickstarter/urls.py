from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from kickstarter import views
from django.contrib import admin
admin.autodiscover()

#handler404 = views.handler404

urlpatterns = patterns('kickstarter.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^servers$', 'server_view', name='server_view'),
                       url(r'^settings$', 'settings_view', name='settings_view'),
                       url(r'^settings/add$', 'settings_add', name='settings_add'),
                   )

urlpatterns += staticfiles_urlpatterns()

