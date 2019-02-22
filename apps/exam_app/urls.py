from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new$', views.new_trip),
    url(r'^create_trip$', views.create_trip),
    url(r'^update_trip$', views.update_trip),
    url(r'^trips/edit/(?P<id>\d+)$', views.edit_trip),
    url(r'^trips/(?P<id>\d+)/delete$', views.delete_trip),
    url(r'^trips/(?P<id>\d+)$', views.view_trip),
    url(r'^join_trip/(?P<id>\d+)$', views.join_trip),
    url(r'^cancel_trip/(?P<id>\d+)$', views.cancel_trip),
]