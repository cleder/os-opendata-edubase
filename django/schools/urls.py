from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
     url(r'^schools-in', views.SchoolsInArea.as_view(), name='schools-in'),
    #url(r'^compute/$', views.auto_assign, name='compute'),
    url(r'^logout/$', views.logout, name='logout'),
    #url(r'^stopwords/$', views.stopwords, name='stopwords'),
    url(r'^assign-around/$', views.start_at_location, name='start-at-location'),
    url(r'^import-log/$', views.ImportList.as_view(), name='import-log'),
    url(r'^os-school/(?P<gid>[0-9]+)/$', views.OsSchoolGeoJsonView.as_view(), name='os-school'),
    url(r'^assign/$', views.start_noosm_at_random, name='start-assign-os-school'),
    url(r'^assign/(?P<gid>[0-9]+)/$', views.AssignPolyToSchoolNoOsm.as_view(), name='assign-os-school'),
    url(r'^assign-all/$', views.start_all_at_random, name='start-assign-all'),
    url(r'^assign-all/(?P<gid>[0-9]+)/$', views.AssignPolyToSchool.as_view(), name='assign-all'),
    url(r'^assign-around/(?P<gid>[0-9]+)/$', views.AssignPolyToSchoolAround.as_view(), name='assign-around'),
    url(r'^edubase-schools/(?P<gid>[0-9]+)/$', views.SchoolNameGeoJsonView.as_view(), name='edubase-schools'),
    url(r'^osm-schools/(?P<gid>[0-9]+)/$', views.OsmSchoolPolyGeoJsonView.as_view(), name='osm-schools'),
    url(r'^osm-schoollines/(?P<gid>[0-9]+)/$', views.OsmSchoolLineGeoJsonView.as_view(), name='osm-schoollines'),
    url(r'^osm-schoolmlines/(?P<gid>[0-9]+)/$', views.OsmSchoolMultiLinesGeoJsonView.as_view(), name='osm-schoolmlines'),
    url(r'^osm-schoolpointss/(?P<gid>[0-9]+)/$', views.OsmSchoolPointGeoJsonView.as_view(), name='osm-schoolpoints'),
    ]
