from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compute/$', views.compute, name='compute'),
    url(r'^logout/$', views.logout, name='logout'),
    ]
