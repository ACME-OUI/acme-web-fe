from django.conf.urls import patterns, include, url

from acme_site import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<acme>\d+)/$', views.index, name='index'),
    url(r'^login/?$', views.user_login, name='login'),
    url(r'^add_credentials/', views.add_credentials),
    url(r'^logout/?$', views.user_logout, name='logout'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^workflow/?$', views.workflow),
    url(r'^jspanel/?$', views.jspanel, name='jspanel'),
    url(r'^grid/?$', views.grid, name='grid'),
    
    url(r'^issues/?$', views.issues, name='issues'),
    url(r'^save_layout/', views.save_layout, name='save_layout'),
    url(r'^load_layout/', views.load_layout, name='load_layout'),
    url(r'^node_info/', views.node_info),
    url(r'^node_search/', views.node_search),
    url(r'^velo/', views.velo),

    #Demo Pages 03/2013
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


