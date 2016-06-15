#
from collections import Counter
import json, random
from operator import itemgetter
import urllib
from urlparse import urlparse

import Levenshtein
from django.db import connection
from django.conf import settings
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as TheDistance
from django.contrib.gis import geos
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic import View

from djgeojson.views import GeoJSONResponseMixin
import phonenumbers
from pygeoif import MultiPolygon, Polygon, Point

from .models import  EducationSite, Postcodes
from .models import ImportLog, School, SchoolSite
from .models import Points, Lines, Multilinestrings, Multipolygons
from .models import EducationSiteNearSchool, EducationSiteOverlapsOsm
from .utils import tokenize

import osmoapi

open_schools = School.objects.filter(status_name__istartswith = 'open')
school_sites = EducationSite.objects

button_text = 'Add to OSM'

def assign_school_to_site(school,site):
    SchoolSite.objects.create(school=school, site=site)

def get_schools_nearby(geom):
    return (open_schools.filter(location__distance_lte=(geom, Distance(m=250)))
                                    .annotate(distance=TheDistance('location', geom))
                                    .order_by('distance'))

def is_test():
    if 'schools.backends.osm_test.OpenStreetMapTestOAuth' in settings.AUTHENTICATION_BACKENDS:
        return True
    elif 'social.backends.openstreetmap.OpenStreetMapOAuth' in settings.AUTHENTICATION_BACKENDS:
        return False


# simple views
def index(request):
    site_ids = school_sites.values_list('id', flat=True)
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
    for site in school_sites.all():
        count.update(set(tokenize(site.distname)))
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



#class based views
class AssignPolyToSchool(LoginRequiredMixin, TemplateView):

    template_name = "assign.html"

    @property
    def queryset(self):
        if self.location:
            point = geos.Point(self.location['lng'], self.location['lat'])
            return (school_sites.filter(geom__distance_lte=(point, Distance(mi=10)))
                                    .annotate(distance=TheDistance('geom', point))
                                    .order_by('id'))
        else:
            return school_sites

    def tags_for_school(self, school):
        city = school.town or school.locality
        kwargs = dict(amenity='school', name=school.name)
        if school.website:
            kwargs['website'] =  school.website
        kwargs['ref:{0}'.format(school.source.lower())] = str(school.uid)
        kwargs['addr:country'] = 'GB'
        if school.postcode:
            kwargs['addr:postcode'] = school.postcode
        if school.street:
            kwargs['addr:street'] = school.street
        if city:
            kwargs['addr:city'] = city
        if school.phone:
            pn = phonenumbers.parse(school.phone, 'GB')
            kwargs['phone'] = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
        kwargs['source:geometry'] = 'OS Open Map Local'
        kwargs['source:addr'] = school.source.lower()
        kwargs['source:name'] = school.source.lower()
        return kwargs

    def url_for_school(self, school):
        if school.website:
            if school.website.startswith('http'):
                return urlparse(school.website).netloc
            else:
                return school.website

    def get_next_site(self, gid):
        return self.queryset.filter(id__gt=gid).first()

    def get_prev_site(self, gid):
        return self.queryset.filter(id__lt=gid).last()

    def get_location_coockie(self, request):
        lc = request.COOKIES.get('Location')
        if lc:
            self.location = json.loads(urllib.unquote(lc))
        else:
            self.location = None
        return self.location

    def get(self, request, gid):
        self.get_location_coockie(request)
        route = request.resolver_match.url_name
        try:
            site = self.queryset.get(pk=gid)
        except EducationSite.DoesNotExist:
            nextsite = self.get_next_site(gid)
            if nextsite  is None:
                nextsite = self.get_prev_site(gid)
            return HttpResponseRedirect(reverse(route, args=(nextsite.id,)))
        if request.method == 'POST':
            x = site.geom.centroid.x
            y = site.geom.centroid.y
            if is_test():
                url = 'http://api06.dev.openstreetmap.org/edit?#map=18/{0}/{1}'.format(y,x)
            else:
                url = 'http://www.openstreetmap.org/edit?#map=18/{0}/{1}'.format(y,x)
            inject = 'window.open("{0}");'.format(url)
        else:
            inject = ''
        import_logs = site.importlog_set.all()
        schools_nearby = get_schools_nearby(site.geom)
        osm_polys = list(Multipolygons.objects.filter(wkb_geometry__intersects=site.geom).all())
        osm_mls = list(Multilinestrings.objects.filter(wkb_geometry__intersects=site.geom).all())
        osm_ls = list(Lines.objects.filter(wkb_geometry__intersects=site.geom).all())
        osm_pts = list(Points.objects.filter(wkb_geometry__intersects=site.geom).all())
        next_site = self.get_next_site(gid)
        prev_site = self.get_prev_site(gid)
        schools_with_tags = []
        for school in schools_nearby:
            schools_with_tags.append([school,
                                      self.tags_for_school(school),
                                      self.url_for_school( school)])
        context = {'site': site,
                   'schools_nearby': schools_with_tags,
                   'osm_polys': osm_polys + osm_mls + osm_ls + osm_pts,
                   'next_site': next_site,
                   'prev_site': prev_site,
                   'button_text': button_text,
                   'import_logs': import_logs,
                   'route': route,
                   'inject_js': inject,}
        return self.render_to_response(context)

    def post(self, request, gid):
        self.get_location_coockie(request)
        site = self.queryset.get(pk=gid)
        mp = MultiPolygon([Polygon(c) for c in site.geom.coords])
        test = is_test()
        idx = None
        for v, k in request.POST.items():
            if k == button_text:
                idx = int(v)
        if idx is not None:
            school = open_schools.get(pk=idx)
            access_token = request.user.social_auth.first().access_token
            api = osmoapi.OSMOAuthAPI(
                    client_key= settings.SOCIAL_AUTH_OPENSTREETMAP_KEY,
                    client_secret=settings.SOCIAL_AUTH_OPENSTREETMAP_SECRET,
                    resource_owner_key=access_token['oauth_token'],
                    resource_owner_secret=access_token['oauth_token_secret'],
                    test = test)
            cs = api.create_changeset('osmoapi', 'Testing oauth api')
            point = Point(school.location.coords)
            change = osmoapi.OsmChange(cs)
            city = school.town or school.locality
            kwargs = self.tags_for_school(school)
            if (site.cleaned_name_no_type and
                school.cleaned_name_no_type and
                site.cleaned_name_no_type != school.cleaned_name_no_type):
                kwargs['alt_name'] = site.distname
            change.create_multipolygon(mp, **kwargs)
            api.diff_upload(change)
            assert api.close_changeset(cs)
            logentry = ImportLog(school=school, site=site,
                                 user=request.user, changeset=cs.id,
                                 change = change.to_string())
            logentry.save()
        return self.get(request, gid)

class AssignPolyToSchoolNoOsm(AssignPolyToSchool):

    @property
    def queryset(self):
        includes = EducationSiteNearSchool.objects.values_list('site_id', flat=True)
        excludes = EducationSiteOverlapsOsm.objects.values_list('site_id', flat=True)
        include_only = set(includes)-set(excludes)
        if self.location:
            point = geos.Point(self.location['lng'], self.location['lat'])
            return (school_sites.filter(geom__distance_lte=(point, Distance(mi=10)))
                                .filter(id__in=include_only)
                                .annotate(distance=TheDistance('geom', point))
                                .order_by('distance'))
        else:
            return school_sites.filter(id__in=include_only)

class OsSchoolGeoJsonView(GeoJSONResponseMixin, View):

    def get_queryset(self):
        return school_sites.filter(pk=self.gid)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)


class SchoolNameGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'location'
    properties = ['schoolname']

    def get_queryset(self):
        site = school_sites.get(pk=self.gid)
        return get_schools_nearby(site.geom)


    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)

class OsmSchoolPolyGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'wkb_geometry'

    def get_queryset(self):
        site = school_sites.get(pk=self.gid)
        return Multipolygons.objects.filter(wkb_geometry__intersects=site.geom)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)


class OsmSchoolLineGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'wkb_geometry'

    def get_queryset(self):
        site = school_sites.get(pk=self.gid)
        return Lines.objects.filter(wkb_geometry__intersects=site.geom)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)

class OsmSchoolMultiLinesGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'wkb_geometry'

    def get_queryset(self):
        site = school_sites.get(pk=self.gid)
        return Multilinestrings.objects.filter(wkb_geometry__intersects=site.geom)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)



class OsmSchoolPointGeoJsonView(GeoJSONResponseMixin, View):

    geometry_field = 'wkb_geometry'
    properties = {'name': 'schoolname'}

    def get_queryset(self):
        site = school_sites.get(pk=self.gid)
        #return Points.objects.filter(wkb_geometry__distance_lte=(site.geom, Distance(m=25)))
        return Points.objects.filter(wkb_geometry__intersects=site.geom)

    def get(self, request, gid):
        self.gid = gid
        return self.render_to_response(None)
