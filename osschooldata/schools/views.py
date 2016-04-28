#
from collections import Counter
import json
from operator import itemgetter

import Levenshtein
from django.db import connection

from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as TheDistance
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View

from djgeojson.views import GeoJSONResponseMixin

from .models import Edubase, FunctionalSite, Postcodes, SeedData
from .models import School, SchoolSite
from .utils import tokenize


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
     return render(request, 'home.html')


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
            print 'FAIL'


#class based views
class AssignPolyToSchool(TemplateView):
    template_name = "assign.html"

    def get(self, request, gid):
        site = school_sites.get(gid=gid)
        next_site = school_sites.filter(gid__gt=gid).first()
        prev_site = school_sites.filter(gid__lt=gid).last()
        context = {'site': site, 'next_site': next_site, 'prev_site': prev_site}
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
