from django.conf.urls import url
from transfer import views

urlpatterns = [
    url(r'^view_remote_directory/$', views.view_remote_directory, name='view_remote_directory'),
    url(r'^nersc_login/$', views.nersc_login),
    url(r'^nersc_credential_check$', views.nersc_credential_check),
]
