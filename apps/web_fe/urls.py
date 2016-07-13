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
                       url(r'^credential_check_existance/', views.credential_check_existance),
                       url(r'^save_layout/', views.save_layout, name='save_layout'),
                       url(r'^load_layout/', views.load_layout, name='load_layout'),
                       url(r'^userdata/image/(?P<path>.*\.png)$', views.send_image),
                       )

urlpatterns += staticfiles_urlpatterns()
