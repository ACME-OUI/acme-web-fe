from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^acme/', include('web_fe.urls')),
    url(r'^poller/', include('poller.urls')),
    url(r'^run_manager/', include('run_manager.urls')),
    url(r'^esgf/', include('esgf.urls')),
    url(r'^cdat/', include('cdat.urls'))
]
