from django.conf.urls import patterns, include, url

from acme_site import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^acme/(?P<acme>\d+)/$', views.index),
    url(r'^login/?$', views.login),
    url(r'^workflow/?$', views.workflow),
    
    url(r'^code/?$', views.code),
    url(r'^config/?$', views.config),
    url(r'^inputs/?$', views.inputs),
    url(r'^build/?$', views.build),
    url(r'^run/?$', views.run),
    url(r'^output/?$', views.output),
    
    #ajax
    url(r'^gettemplates/?$', views.gettemplates),
    url(r'^clonetemplates/?$', views.clonetemplates),
    url(r'^getchildren/?$', views.getchildren),
    url(r'^getfile/?$', views.getfile),
    url(r'^savefile/?$', views.savefile),
    url(r'^getresource/?$', views.getresource),
     
    url(r'^filetree/?$', views.filetree),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()


