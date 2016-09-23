from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include, url
from web_fe import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<acme>\d+)/$', views.index, name='index'),
    url(r'^login/?$', views.user_login, name='login'),
    url(r'^add_credentials/', views.add_credentials, name='add_credentials'),
    url(r'^check_credentials/', views.check_credentials, name='check_credentials'),
    url(r'^logout/?$', views.user_logout, name='logout'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^dashboard/?$', views.dashboard, name='dashboard'),
    url(r'^credential_check_existance/', views.credential_check_existance, name='credential_check_existance'),
    url(r'^save_layout/', views.save_layout, name='save_layout'),
    url(r'^load_layout/', views.load_layout, name='load_layout'),
    url(r'^userdata/image/(?P<path>.*[\.png|\.svg|\.pdf])$', views.send_image, name='send_image'),
    url(r'^get_notification_list/$', views.get_notification_list),
]

urlpatterns += staticfiles_urlpatterns()
