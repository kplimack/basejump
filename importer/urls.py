from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from kickstarter import views
from django.contrib import admin
admin.autodiscover()

#handler404 = views.handler404

urlpatterns = patterns('importer.views',
                       url(r'^$', 'index', name='index'),
                   )

urlpatterns += staticfiles_urlpatterns()

