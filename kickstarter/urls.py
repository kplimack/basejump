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
                       url(r'^ksconfig/(?P<opsys>\w+)/(?P<release>.+)/(?P<arch>\w+)/(?P<hostname>.+)$', 'get_ksconfig', name='get_ksconfig'),
                       url(r'^kickme/(?P<opsys>\w+)/(?P<release>.+)/(?P<arch>\w+)$', 'kickme', name='kickme'),
                       url(r'^seedme/(?P<opsys>\w+)/(?P<release>.+)/(?P<arch>\w+)$', 'seedme', name='seedme'),
                       url(r'imdone/(?P<asset_id>\w+)$', 'servers_release', name='servers_release'),
                       url(r'^servers$', 'server_view', name='server_view'),
                       url(r'^settings$', 'settings_view', name='settings_view'),
                       url(r'^servers/kick$', 'servers_kick', name='servers_kick'),
                       url(r'^BootOptions$', 'bootoptions_view', name='bootoptions_view'),
                       url(r'^BootOptions/add$', 'bootoptions_add', name='bootoptions_add'),
                       url(r'^BootOptions/edit$', 'bootoptions_edit', name='bootoptions_edit'),
                       url(r'^BootOptions/get/assetid/(?P<asset_id>\w+)$', 'bootoptions_get_assetid', name='bootoptions_get_assetid'),
                       url(r'^BootOptions/get/macaddr/(?P<macaddr>\w+)$', 'bootoptions_get_macaddr', name='bootoptions_get_macaddr'),
                       url(r'^settings/add$', 'settings_add', name='settings_add'),
                       url(r'^chef/validator$', 'chef_validator', name='chef_validator'),
                       url(r'^chef/client$', 'chef_client', name='chef_client'),
                       url(r'^GetRepo/(?P<reponame>.+)$', 'get_repo', name='get_repo')
                   )

urlpatterns += staticfiles_urlpatterns()

