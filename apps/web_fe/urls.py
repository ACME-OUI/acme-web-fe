from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from web_fe import views
from esgf import views as esgf_views
from cdat import views as cdat_views
from run_manager import views as run_views


run_patterns = [
    url(r'^create_run/$', run_views.create_run),
    url(r'^view_runs/$', run_views.view_runs),
    url(r'^delete_run/$', run_views.delete_run),
    url(r'^create_script/$', run_views.create_script),
    url(r'^get_scripts/$', run_views.get_scripts),
    url(r'^update_script/$', run_views.update_script),
    url(r'^read_script/$', run_views.read_script),
    url(r'^delete_script/$', run_views.delete_script),
    url(r'^get_templates/$', run_views.delete_script),
]

esgf_patterns = [
    # url(r'^node_info/$', esgf_views.node_info),
    url(r'^node_search/$', esgf_views.node_search),
    url(r'^load_facets/$', esgf_views.load_facets),
    url(r'^download/$', esgf_views.download),
    url(r'^logon/$', esgf_views.logon),
    url(r'^node_list/$', esgf_views.node_list),
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
                       url(r'^run_manager/', include(run_patterns)),
                       url(r'^esgf/', include(esgf_patterns)),
                       url(r'^cdat/', include(cdat_patterns)),
                       )

urlpatterns += staticfiles_urlpatterns()
