from django.conf.urls import patterns, url
from cdat import views


urlpatterns = patterns( '',
                        url(r'^vtk/', views.vtkweb_launcher),
                        url(r'^_refresh', views._refresh),
                        url(r'^vtk_viewer', views.vtk_viewer),
                        url(r'^vtk_test', views.vtk_test),
                        )
