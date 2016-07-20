from django.conf.urls import patterns, url
from esgf import views

urlpatterns = patterns( '',
                        url(r'^node_search/$', views.node_search),
                        url(r'^load_facets/$', views.load_facets),
                        url(r'^download/$', views.download),
                        url(r'^logon/$', views.logon),
                        url(r'^node_list/$', views.node_list),
                        )
