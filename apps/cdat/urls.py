from django.conf.urls import url
from cdat import views


urlpatterns = [
    url(r'^vtk/', views.vtkweb_launcher),
    url(r'^_refresh', views._refresh),
    url(r'^vtk_viewer', views.vtk_viewer),
    url(r'^vtk_test', views.vtk_test),
]
