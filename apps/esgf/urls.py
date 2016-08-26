from django.conf.urls import url
from esgf import views

urlpatterns = [
    url(r'^node_search/$', views.node_search),
    url(r'^load_facets/$', views.load_facets),
    url(r'^download/$', views.download),
    url(r'^logon/$', views.logon),
    url(r'^node_list/$', views.node_list),
    url(r'^get_user_data$', views.get_user_data),
    url(r'^file_upload/$', views.file_upload),
]
