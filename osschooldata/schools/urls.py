from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compute/$', views.auto_assign, name='compute'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^stopwords/$', views.stopwords, name='stopwords'),
    url(r'^os-school/(?P<gid>[0-9]+)/$', views.OsSchoolGeoJsonView.as_view(), name='os-school'),
    url(r'^assign/(?P<gid>[0-9]+)/$', views.AssignPolyToSchool.as_view(), name='assign-os-school'),
    url(r'^edubase-schools/(?P<gid>[0-9]+)/$', views.SchoolNameGeoJsonView.as_view(), name='edubase-schools'),
    url(r'^osm-schools/(?P<gid>[0-9]+)/$', views.OsmSchoolGeoJsonView.as_view(), name='osm-schools'),
    ]
