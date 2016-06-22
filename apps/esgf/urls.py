from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^node_info/', views.node_info),
    url(r'^node_search/', views.node_search),
    url(r'^load_facets/', views.load_facets),
)
