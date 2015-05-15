from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^questions/create/?$', views.create_question),
    url(r'^questions/delete/(\d+)/?$', views.delete_question),
    url(r'^questions/edit/(\d+)/?$', views.edit_question),
    url(r'^questions/([^/]+)/?$', views.show_question)
)
