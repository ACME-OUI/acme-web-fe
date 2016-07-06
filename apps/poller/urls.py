from django.conf.urls import url

from poller import views

urlpatterns = [
    url(r'^update/$', views.update, name='update')
]
