#
from operator import itemgetter

import Levenshtein
from django.db import connection

from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as TheDistance
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse

from .models import Edubase, FunctionalSite, Postcodes, SeedData
from .models import EdubaseSite, SeedSite


def index(request):
     return render(request, 'home.html')

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


#filter(location__distance_lte=(poly, Distance(m=150))).distance(poly).annotate(distance=Distance('location', poly)).order_by('distance').all()

def compute(request):
    response = "Home."
    cursor = connection.cursor()
    cursor.execute('SELECT site_id FROM schools_edubasesite UNION SELECT site_id FROM schools_seedsite;')
    sites_to_exclude=[row[0] for row in cursor.fetchall()]
    sites = FunctionalSite.objects.filter(sitetheme = 'Education').exclude(gid__in=sites_to_exclude)
    cursor.execute('SELECT school_id FROM schools_edubasesite;')
    edu_schools_to_exclude=[row[0] for row in cursor.fetchall()]
    edu_schools = Edubase.objects.filter(establishmentstatus_name = 'Open').exclude(urn__in=edu_schools_to_exclude)
    cursor.execute('SELECT school_id FROM schools_seedsite;')
    seed_schools_to_exclude=[row[0] for row in cursor.fetchall()]
    seed_schools = SeedData.objects.exclude(id__in=seed_schools_to_exclude)
    num_schools=seed_schools.count() + edu_schools.count()
    i = 0
    successfuls = 0
    failures = 0
    num_sites=sites.count()
    print 'sites found', num_sites
    for site in sites.all():
        i+=1
        print "{0} of {1} sites scanned {2} success {3} failure".format(i, num_sites, successfuls, failures)
        poly = site.geom
        school_sites = []
        for school in edu_schools.filter(location__distance_lte=(poly, Distance(m=150))).annotate(distance=TheDistance('location', poly)).order_by('distance').all():
            if school.establishmentname != site.distname:
                print school.establishmentname, site.distname
                if school.establishmentname and  site.distname:
                    school_sites.append([Levenshtein.ratio(school.establishmentname, site.distname), school, site])
            else:
                print 'success'
                EdubaseSite.objects.create(school=school, site=site)
                successfuls+=1
                break
        else:
            if school_sites:
                a = sorted(school_sites, key=itemgetter(1))
                if a[0][0] > 0.7 :
                    EdubaseSite.objects.create(school=a[0][1], site=a[0][2])
                    successfuls+=1
                else:
                    failures+=1
                    print 'failed for', site.distname
        school_sites = []
        for school in seed_schools.filter(location__distance_lte=(poly, Distance(m=150))).annotate(distance=TheDistance('location', poly)).order_by('distance').all():
            if school.schoolname != site.distname:
                if school.schoolname and  site.distname:
                    school_sites.append([Levenshtein.ratio(school.schoolname, site.distname), school, site])
            else:
                print 'success'
                SeedSite.objects.create(school=a[0][1], site=a[0][2])
                successfuls+=1
                break
        else:
            if school_sites:
                a = sorted(school_sites, key=itemgetter(1))
                if a[0][0] > 0.7 :
                    SeedSite.objects.create(school=a[0][1], site=a[0][2])
                    successfuls+=1
                else:
                    failures+=1
                    print 'failed for', site.distname
    return HttpResponse(response)
