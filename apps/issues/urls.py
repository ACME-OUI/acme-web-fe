from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^/?$', views.issue_form),
    url(r'^confirm/?$', views.confirm_email),
    url(r'^confirm/subscription/?$', views.confirm_subscription),
    url(r'^issue/submit/?$', views.make_issue),
    url(r'^subscriptions/remove/?$', views.remove_subscription),
    url(r'^question/(\d+)/next$', views.get_next),
    url(r'^questions/create/?$', views.create_question),
    url(r'^questions/delete/(\d+)/?$', views.delete_question),
    url(r'^questions/edit/(\d+)/?$', views.edit_question),
    url(r'^questions/([^/]+)/?$', views.show_question)
)
