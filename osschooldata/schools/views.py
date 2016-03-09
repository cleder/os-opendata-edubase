#
from operator import itemgetter

import Levenshtein

from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as TheDistance
from django.shortcuts import render
from django.http import HttpResponse

from .models import Edubase, FunctionalSite, Postcodes, SeedData
from .models import EdubaseSite, SeedSite

#filter(location__distance_lte=(poly, Distance(m=150))).distance(poly).annotate(distance=Distance('location', poly)).order_by('distance').all()

def index(request):
    response = "Home."
    sites = FunctionalSite.objects.filter(sitetheme = 'Education')
    edu_schools = Edubase.objects.filter(establishmentstatus_name = 'Open')
    seed_schools = SeedData.objects
    num_sites=sites.count()
    i = j = k = 0
    print 'sites found', num_sites
    for site in sites.all():
        i+=1

        print "{0} of {1} sites scanned {2} success {3} failure".format(i, num_sites, j, k)
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
                j+=1
                break
        else:
            if school_sites:
                a = sorted(school_sites, key=itemgetter(1))
                if a[0][0] > 0.7 :
                    EdubaseSite.objects.create(school=a[0][1], site=a[0][2])
                    j+=1
                else:
                    k+=1
                    print 'failed for', site.distname
        school_sites = []
        for school in seed_schools.filter(location__distance_lte=(poly, Distance(m=150))).annotate(distance=TheDistance('location', poly)).order_by('distance').all():
            if school.schoolname != site.distname:
                print school.schoolname, site.distname
                if school.schoolname and  site.distname:
                    print Levenshtein.ratio(school.schoolname, site.distname)
            else:
                print 'success'
                SeedSite.objects.create(school=a[0][1], site=a[0][2])
                j+=1
                break
        else:
            if school_sites:
                a = sorted(school_sites, key=itemgetter(1))
                if a[0][0] > 0.7 :
                    SeedSite.objects.create(school=a[0][1], site=a[0][2])
                    j+=1
                else:
                    k+=1
                    print 'failed for', site.distname
    return HttpResponse(response)
