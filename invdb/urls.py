from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from invdb import views
from django.contrib import admin
admin.autodiscover()

#handler404 = views.handler404

urlpatterns = patterns('invdb.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^area_add', 'area_add', name='area_add'),
                       url(r'^asset_add', 'asset_add', name='asset_add'),
                   )

urlpatterns += staticfiles_urlpatterns()

