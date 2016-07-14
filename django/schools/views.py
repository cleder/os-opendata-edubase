#
import json
import random
import urllib
from collections import Counter
from operator import itemgetter
from urlparse import urlparse

import osmoapi
import phonenumbers
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis import geos
from django.contrib.gis.db.models.functions import Distance as TheDistance
from django.contrib.gis.measure import Distance
from django.core.urlresolvers import reverse
from django.db import connection
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View
from djgeojson.views import GeoJSONResponseMixin
from pygeoif import MultiPolygon
from pygeoif import Point
from pygeoif import Polygon

from .forms import SiteCommentForm
from .models import EducationSite
from .models import EducationSiteNearSchool
from .models import EducationSiteOverlapsOsm
from .models import ImportLog
from .models import Lines
from .models import Multilinestrings
from .models import Multipolygons
from .models import Points
from .models import Postcodes
from .models import School
from .models import SchoolSite
from .models import SiteComment
from .utils import tokenize

open_schools = School.objects.filter(status_name__istartswith = 'open')
school_sites = EducationSite.objects

BUTTON_TEXT = 'Add to OSM'

def get_location_coockie(request):
    location = None
    lc = request.COOKIES.get('Location')
    if lc:
        location = json.loads(urllib.unquote(lc))
    return location

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

def url_for_school(school):
    if school.website:
        if school.website.startswith('http'):
            return urlparse(school.website).netloc
        else:
            return school.website


# simple views
def index(request):
    return render(request, 'home.html')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


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

def start_at_location(request):
    location = get_location_coockie(request)
    if location:
        point = geos.Point(location['lng'], location['lat'])
        start_school = (school_sites.filter(geom__distance_lte=(point, Distance(mi=1)))
                                    .annotate(distance=TheDistance('geom', point))
                                    .order_by('distance')).first()
        if not start_school:
            msg = 'There are no schools in a one mile radius from the location you chose!'
            messages.info(request, msg)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(reverse('assign-around', args=(start_school.id,)))
    else:
        msg = 'Please add the location around which you want to map by clicking on the map!'
        messages.info(request, msg)
        return HttpResponseRedirect('/')

def start_all_at_random(request):
    site_id = random.choice(school_sites.values_list('id', flat=True))
    return HttpResponseRedirect(reverse('assign-all', args=([site_id, ])))

def start_noosm_at_random(request):
    site = random.choice(list(EducationSite.objects.raw('select id from importable_site_no_osm')))
    return HttpResponseRedirect(reverse('assign-os-school', args=([site.pk, ])))


#class based views
class AssignPolyToSchool(LoginRequiredMixin, TemplateView):

    template_name = 'assign.html'

    @property
    def queryset(self):
        return school_sites

    def tags_for_school(self, school):
        city = school.town or school.locality
        kwargs = dict(amenity='school', name=school.name)
        if school.website:
            kwargs['website'] =  url_for_school(school)
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


    def get_next_site(self, gid):
        return self.queryset.filter(id__gt=gid).first()

    def get_prev_site(self, gid):
        return self.queryset.filter(id__lt=gid).last()

    def get(self, request, gid):
        if is_test():
            msg = ('This site is currently in test mode all additions will'
                   ' be made to api06.dev.openstreetmap.org - not the live server!')
            messages.warning(request, msg)
        self.location = get_location_coockie(request)
        route = request.resolver_match.url_name
        try:
            site = school_sites.get(pk=gid)
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
        comments = site.sitecomment_set.all()
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
                                      url_for_school( school)])
        comment_form = SiteCommentForm()
        context = {'site': site,
                   'schools_nearby': schools_with_tags,
                   'osm_polys': osm_polys + osm_mls + osm_ls + osm_pts,
                   'next_site': next_site,
                   'prev_site': prev_site,
                   'button_text': BUTTON_TEXT,
                   'import_logs': import_logs,
                   'route': route,
                   'comment_form': comment_form,
                   'comments' : comments,
                   'inject_js': inject,}
        return self.render_to_response(context)

    def post(self, request, gid):
        self.location = get_location_coockie(request)
        site = school_sites.get(pk=gid)
        mp = MultiPolygon([Polygon(c) for c in site.geom.coords])
        test = is_test()
        idx = None
        for v, k in request.POST.items():
            if k == BUTTON_TEXT:
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
            kwargs = self.tags_for_school(school)
            msg = 'Added School {0} in {1}, UK via http://schools.mapthe.uk'.format(
                kwargs.get('name', ''), kwargs.get('addr:city', ''))
            cs = api.create_changeset('schools.mapthe.uk', msg)
            point = Point(school.location.coords)
            change = osmoapi.OsmChange(cs)
            if (site.cleaned_name_no_type and
                school.cleaned_name_no_type and
                site.cleaned_name_no_type != school.cleaned_name_no_type):
                kwargs['alt_name'] = site.distname
            change.create_multipolygon(mp, **kwargs)
            result = api.diff_upload(change)
            assert api.close_changeset(cs)
            logentry = ImportLog(school=school, site=site,
                                 user=request.user, changeset=cs.id,
                                 change = change.to_string() + result)
            logentry.save()
        elif 'submit-comment' in request.POST.keys():
            form = SiteCommentForm(request.POST)
            if form.is_valid():
                comment = SiteComment(user=request.user, site=site, **form.cleaned_data)
                comment.save()
        else:
            msg = 'oops something went wrong - please try again'
            messages.error(request, msg)
        return self.get(request, gid)


class AssignPolyToSchoolAround(AssignPolyToSchool):

    @property
    def queryset(self):
        point = geos.Point(self.location['lng'], self.location['lat'])
        return (school_sites.filter(geom__distance_lte=(point, Distance(mi=10)))
                                .annotate(distance=TheDistance('geom', point))
                                .order_by('distance'))

    def get_next_site(self, gid):
        is_next = False
        next_site = None
        for site in self.queryset:
            next_site = site
            if is_next:
                break
            if site.id == int(gid):
                is_next = True
        return next_site

    def get_prev_site(self, gid):
        prev_site = None
        for site in self.queryset:
            if site.id == int(gid):
                break
            prev_site = site
        return prev_site


class AssignPolyToSchoolNoOsm(AssignPolyToSchool):

    @property
    def queryset(self):
        return EducationSite.objects.raw('SELECT * FROM importable_site_no_osm')

    def get_next_site(self, gid):
        return EducationSite.objects.raw(
            'SELECT * FROM importable_site_no_osm WHERE id > %s LIMIT 1',
            [gid, ])[0]

    def get_prev_site(self, gid):
        return EducationSite.objects.raw(
            'SELECT * FROM importable_site_no_osm WHERE id < %s ORDER BY id DESC LIMIT 1',
            [gid, ])[0]


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
