from django.contrib.gis import admin

from .models import Fhrs

class FhrsAdmin(admin.GeoModelAdmin):
    list_display=['fhrs_id', 'business_name', 'business_type', 'postcode']
    search_fields = ['postcode', 'business_name']

admin.site.register(Fhrs, FhrsAdmin)
