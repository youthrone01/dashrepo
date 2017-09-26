from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/admin$', views.admin),
    url(r'^users/new$', views.add_new),
    url(r'^users/edit$', views.edit),
    url(r'^users/edit/(?P<user_id>[0-9]+)$', views.user_edit),
    url(r'^users/show/(?P<user_id>[0-9]+)$', views.show_user),
    url(r'^logoff$', views.logoff),
]