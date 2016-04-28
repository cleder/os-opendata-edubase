# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis import admin
from .models import Edubase, FunctionalSite, Postcodes, SeedData, School

admin.site.register(Edubase, admin.GeoModelAdmin)
admin.site.register(FunctionalSite, admin.GeoModelAdmin)
admin.site.register(Postcodes, admin.GeoModelAdmin)
admin.site.register(SeedData, admin.GeoModelAdmin)
admin.site.register(School, admin.GeoModelAdmin)
