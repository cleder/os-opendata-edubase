from django.contrib.gis.db import models

from . import api

class Fhrs(models.Model):

    fhrs_id = models.IntegerField(unique=True)
    business_name = models.TextField(blank=True, null=True)
    business_type = models.TextField(blank=True, null=True)
    address_line1 = models.TextField(blank=True, null=True)
    address_line2 = models.TextField(blank=True, null=True)
    address_line3 = models.TextField(blank=True, null=True)
    address_line4 = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=8, blank=True, null=True)
    location = models.PointField(blank=True, null=True)


def fhrs_import(local_authority_id):
    establisments = api.get_establishments(local_authority_id)
    for est in establisments:
        ed = api.parse_establishment(est)
        Fhrs.objects.create(**ed)

