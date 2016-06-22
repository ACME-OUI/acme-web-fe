from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^vtk/', views.vtkweb_launcher),
)
