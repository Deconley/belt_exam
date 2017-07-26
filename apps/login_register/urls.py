
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^createItem$', views.createItem),
    url(r'^addItem$', views.addItem),
    url(r'^item_info/(?P<id>\d+)$', views.item_info),
    
]
