from django.conf.urls import url
from esgf import views

urlpatterns = [
    url(r'^node_search/$', views.node_search),
    url(r'^load_facets/$', views.load_facets),
    url(r'^logon/$', views.logon),
    url(r'^node_list/$', views.node_list),
    url(r'^get_user_data$', views.get_user_data),
    url(r'^file_upload/$', views.file_upload),
    url(r'^get_publish_config/$', views.get_publish_config),
    url(r'^get_publish_config_list/$', views.get_publish_config_list),
    url(r'^save_publish_config/$', views.save_publish_config),
    url(r'^publish/$', views.publish),
    url(r'^upload_to_viewer/$', views.upload_to_viewer),
    url(r'^get_favorite_plots/$', views.get_favorite_plots),
    url(r'^set_favorite_plot/$', views.set_favorite_plot),
    url(r'^read_nc/$', views.read_nc),
]
