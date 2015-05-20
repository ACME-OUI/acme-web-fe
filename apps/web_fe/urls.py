from django.conf.urls import patterns, include, url

from web_fe import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<acme>\d+)/$', views.index, name='index'),
                       url(r'^login/?$', views.user_login, name='login'),
                       url(r'^add_credentials/', views.add_credentials),
                       url(r'^check_credentials/', views.check_credentials),
                       url(r'^logout/?$', views.user_logout, name='logout'),
                       url(r'^register/?$', views.register, name='register'),
                       url(r'^workflow/?$', views.workflow),
                       url(r'^grid/?$', views.grid, name='grid'),
                       url(r'^credential_check_existance/', view.credential_check_existance),
                       url(r'^get_home_folder/', views.get_home_folder),

                       url(r'^save_layout/', views.save_layout,
                           name='save_layout'),
                       url(r'^load_layout/', views.load_layout,
                           name='load_layout'),
                       url(r'^node_info/', views.node_info),
                       url(r'^node_search/', views.node_search),
                       url(r'^velo/', views.velo),


                       # ajax
                       url(r'^gettemplates/?$', views.gettemplates),
                       url(r'^clonetemplates/?$', views.clonetemplates),
                       url(r'^getchildren/?$', views.getchildren),
                       url(r'^getfile/?$', views.getfile),
                       url(r'^savefile/?$', views.savefile),
                       url(r'^getresource/?$', views.getresource),

                       url(r'^filetree/?$', views.filetree),
                       )

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
