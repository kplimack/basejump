from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
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
                       url(r'^assets/edit/(?P<asset_id>\w+)$', 'asset_edit', name='asset_edit'),
                       url(r'^interfaces/edit/(?P<interface_id>\w+)$', 'interface_edit', name='interface_edit'),
                       url(r'^assets/edit/(?P<asset_id>\w+)/interface_add$', 'interface_add', name='interface_add'),
                       url(r'^assets$', 'asset_view', name='asset_view'),
                       url(r'^assets/(?P<asset_type>\w+)', 'asset_view', name='asset_view'),
#                       url(r'^assets/edit/(?P<asset_type>\w+)$', 'asset_edit', name='asset_edit'),
                   )

urlpatterns += staticfiles_urlpatterns()

