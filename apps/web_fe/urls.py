from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from web_fe import views
from velo import views as velo_views
from esgf import views as esgf_views
from cdat import views as cdat_views

velo_patterns = [
    url(r'^get_folder/$', velo_views.get_folder),
    url(r'^get_file/$', velo_views.get_file),
    url(r'^velo_save_file/$', velo_views.save_file),
    url(r'^velo_new_folder/$', velo_views.new_folder),
    url(r'^velo_delete/$', velo_views.delete),
]

esgf_patterns = [
    url(r'^node_info/$', esgf_views.node_info),
    url(r'^node_search/$', esgf_views.node_search),
    url(r'^load_facets/$', esgf_views.load_facets),
    url(r'^download/$', esgf_views.download),
    url(r'^logon/$', esgf_views.logon),
]

cdat_patterns = [
    url(r'^vtk/', cdat_views.vtkweb_launcher),
    url(r'^_refresh', cdat_views._refresh),
    url(r'^vtk_viewer', cdat_views.vtk_viewer),
    url(r'^vtk_test', cdat_views.vtk_test),
]

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<acme>\d+)/$', views.index, name='index'),
                       url(r'^login/?$', views.user_login, name='login'),
                       url(r'^add_credentials/', views.add_credentials),
                       url(r'^check_credentials/', views.check_credentials),
                       url(r'^logout/?$', views.user_logout, name='logout'),
                       url(r'^register/?$', views.register, name='register'),
                       url(r'^dashboard/?$', views.dashboard, name='dashboard'),
                       url(r'^credential_check_existance/', views.credential_check_existance),
                       url(r'^save_layout/', views.save_layout, name='save_layout'),
                       url(r'^load_layout/', views.load_layout, name='load_layout'),
                       url(r'^userdata/image/(?P<path>.*\.png)$', views.send_image),
                       url(r'^velo/', include(velo_patterns)),
                       url(r'^esgf/', include(esgf_patterns)),
                       url(r'^cdat/', include(cdat_patterns)),
                       )

urlpatterns += staticfiles_urlpatterns()
