from django.conf.urls import url
from run_manager import views


urlpatterns = [
    url(r'^create_run/$', views.create_run),
    url(r'^view_runs/$', views.view_runs),
    url(r'^delete_run/$', views.delete_run),
    url(r'^start_run/$', views.start_run),
    url(r'^stop_run/$', views.stop_run),
    url(r'^run_status/$', views.run_status),
    url(r'^create_script/$', views.create_script),
    url(r'^get_scripts/$', views.get_scripts),
    url(r'^update_script/$', views.update_script),
    url(r'^read_script/$', views.read_script),
    url(r'^read_output_script/$', views.read_output_script),
    url(r'^delete_script/$', views.delete_script),
    url(r'^get_templates/$', views.get_templates),
    url(r'^copy_template/$', views.copy_template),
    url(r'^get_user/$', views.get_user),
    url(r'^get_output_zip/$', views.get_output_zip),
    url(r'^save_diagnostic_config/$', views.save_diagnostic_config),
    url(r'^get_diagnostic_configs/$', views.get_diagnostic_configs),
    url(r'^get_diagnostic_by_name/$', views.get_diagnostic_by_name),
    url(r'^get_all_configs/$', views.get_all_configs),
    url(r'^get_run_output/$', views.get_run_output),
]
