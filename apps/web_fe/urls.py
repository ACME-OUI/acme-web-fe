from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from web_fe import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<acme>\d+)/$', views.index, name='index'),
                       url(r'^login/?$', views.user_login, name='login'),
                       url(r'^add_credentials/', views.add_credentials),
                       url(r'^check_credentials/', views.check_credentials),
                       url(r'^logout/?$', views.user_logout, name='logout'),
                       url(r'^register/?$', views.register, name='register'),
                       url(r'^dashboard/?$', views.dashboard, name='dashboard'),
                       url(r'^credential_check_existance/',
                           views.credential_check_existance),
                       url(r'^get_folder/', views.get_folder),
                       url(r'^get_file/', views.get_file),
                       url(r'^velo_save_file/', views.velo_save_file),
                       url(r'^velo_new_folder/', views.velo_new_folder),
                       url(r'^velo_delete/', views.velo_delete),

                       url(r'^save_layout/', views.save_layout,
                           name='save_layout'),
                       url(r'^load_layout/', views.load_layout,
                           name='load_layout'),
                       url(r'^node_info/', views.node_info),
                       url(r'^node_search/', views.node_search),
                       url(r'^load_facets/', views.load_facets),
                       url(r'^userdata/image/(?P<path>.*\.png)$', views.send_image),
                       url(r'^vtk/', views.vtkweb_launcher),
                       # url(r'^esgf_download/', views.esgf_download),
                       )

urlpatterns += staticfiles_urlpatterns()
