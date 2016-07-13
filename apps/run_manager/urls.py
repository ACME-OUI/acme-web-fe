from django.conf.urls import patterns, url
from run_manager import views


urlpatterns = patterns('',
        url(r'^create_run/$',  views.create_run),
        url(r'^view_runs/$',  views.view_runs),
        url(r'^delete_run/$',  views.delete_run),
        url(r'^create_script/$',  views.create_script),
        url(r'^get_scripts/$',  views.get_scripts),
        url(r'^update_script/$',  views.update_script),
        url(r'^read_script/$',  views.read_script),
        url(r'^delete_script/$',  views.delete_script),
        url(r'^get_templates/$',  views.get_templates),
        url(r'^copy_template/$', views.copy_template),
    )
