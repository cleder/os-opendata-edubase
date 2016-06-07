# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin
from .models import EducationSite, Postcodes, School, Multipolygons, ImportLog


admin.site.register(EducationSite, admin.GeoModelAdmin)
admin.site.register(Postcodes, admin.GeoModelAdmin)
admin.site.register(School, admin.GeoModelAdmin)
admin.site.register(Multipolygons, admin.GeoModelAdmin)
admin.site.register(ImportLog, admin.GeoModelAdmin)
