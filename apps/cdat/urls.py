from django.conf.urls import url
from cdat import views


urlpatterns = [
    url(r'^get_provenance/$', views.get_provenance),
    url(r'^get_variables/$', views.get_variables),
]
