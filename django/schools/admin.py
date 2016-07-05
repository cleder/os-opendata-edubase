# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin

from .models import EducationSite
from .models import ImportLog
from .models import Lines
from .models import Multilinestrings
from .models import Multipolygons
from .models import Points
from .models import Postcodes
from .models import School


class ImportLogAdmin(admin.ModelAdmin):
    raw_id_fields = ['site', 'school' ]
    list_display = ['user', 'created', 'changeset']
    search_fields = ['user', ]

class EducationSiteAdmin(admin.GeoModelAdmin):
    list_display=['grid_ref', 'distname']
    search_fields = ['grid_ref', 'distname']


class PostcodesAdmin(admin.GeoModelAdmin):
    list_display=['postcode',]
    search_fields = ['postcode',]


class SchoolAdmin(admin.GeoModelAdmin):
    list_display=['source', 'local_authority', 'schoolname', 'postcode']
    search_fields = ['postcode', 'local_authority', 'schoolname']


admin.site.register(EducationSite, EducationSiteAdmin)
admin.site.register(Postcodes, PostcodesAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Multipolygons, admin.GeoModelAdmin)
admin.site.register(Lines, admin.GeoModelAdmin)
admin.site.register(Multilinestrings, admin.GeoModelAdmin)
admin.site.register(Points, admin.GeoModelAdmin)
admin.site.register(ImportLog, ImportLogAdmin)
