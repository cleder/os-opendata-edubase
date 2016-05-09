#
from collections import Counter
import json, random
from operator import itemgetter

import Levenshtein
from django.db import connection
from django.conf import settings
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as TheDistance
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View

from djgeojson.views import GeoJSONResponseMixin
from pygeoif import MultiPolygon, Polygon

from .models import Edubase, FunctionalSite, Postcodes, SeedData
from .models import School, SchoolSite, Multipolygons
from .utils import tokenize

import osmoapi

open_schools = School.objects.filter(status_name__startswith = 'Open')
school_sites = FunctionalSite.objects.filter(sitetheme = 'Education')


def assign_school_to_site(school,site):
    print school.schoolname
    SchoolSite.objects.create(school=school, site=site)

def get_schools_nearby(geom):
    return (open_schools.filter(location__distance_lte=(geom, Distance(m=250)))
                                    .annotate(distance=TheDistance('location', geom))
                                    .order_by('distance'))


# simple views
def index(request):
    site_ids = school_sites.values_list('gid', flat=True)
    context = {'start_site': random.choice(site_ids)}
    return render(request, 'home.html', context=context)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


def stopwords(request):
    count = Counter()
    for school in School.objects.all():
        count.update(set(tokenize(school.schoolname)))
        print school.cleaned_name
        print school.types_from_name
    for site in school_sites.all():
        count.update(set(tokenize(site.distname)))
        print site.cleaned_name
        print site.types_from_name
    response = json.dumps(count.most_common(1000))
    return HttpResponse(response)


def auto_assign(request):
    exclude_sites = SchoolSite.objects.values_list('site_id', flat=True)
    exclude_schools = SchoolSite.objects.values_list('school_id', flat=True)
    for site in school_sites.exclude(gid__in=exclude_sites).all():
        schools = get_schools_nearby(site.geom).exclude(id__in=exclude_schools).all()
        for school in schools:
            if school.schoolname == site.distname:
                assign_school_to_site(school,site)
                continue
            if school.cleaned_name == site.cleaned_name:
                assign_school_to_site(school,site)
                continue
            if school.cleaned_name_no_type == site.cleaned_name_no_type and len(schools)==1:
                assign_school_to_site(school,site)
                continue
        else:
            print 'FAIL'


#class based views
class AssignPolyToSchool(TemplateView):
    template_name = "assign.html"

    def get(self, request, gid):
        site = school_sites.get(gid=gid)
        schools_nearby = get_schools_nearby(site.geom)
        osm_polys = Multipolygons.objects.filter(wkb_geometry__intersects=site.geom)
        next_site = school_sites.filter(gid__gt=gid).first()
        prev_site = school_sites.filter(gid__lt=gid).last()
        mp = MultiPolygon([Polygon(c) for c in site.geom.coords])
        access_token = request.user.social_auth.first().access_token
        api = osmoapi.OSMOAuthAPI(
                client_key= settings.SOCIAL_AUTH_OPENSTREETMAP_KEY,
                client_secret=settings.SOCIAL_AUTH_OPENSTREETMAP_SECRET,
                resource_owner_key=access_token['oauth_token'],
                resource_owner_secret=access_token['oauth_token_secret'])
        #cs = api.create_changeset('osmoapi', 'Testing oauth api')
        #assert api.close_changeset(cs)
        context = {'site': site,
                   'schools_nearby': schools_nearby,
                   'osm_polys': osm_polys,
                   'next_site': next_site,
                   'prev_site': prev_site}
        return self.render_to_response(context)


class OsSchoolGeoJsonView(GeoJSONResponseMixin, View):

    def get_queryset(self):
        return school_sites.filter(gid=self.gid)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)


class SchoolNameGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'location'
    properties = ['schoolname']

    def get_queryset(self):
        site = school_sites.get(gid=self.gid)
        return get_schools_nearby(site.geom)


    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)

class OsmSchoolGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'wkb_geometry'

    def get_queryset(self):
        site = school_sites.get(gid=self.gid)
        return Multipolygons.objects.filter(wkb_geometry__intersects=site.geom)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)
