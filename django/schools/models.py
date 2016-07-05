# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils.functional import cached_property

from .utils import SCHOOL_TYPES
from .utils import STOP_WORDS
from .utils import tokenize


class CleanNameMixIn(object):

    @cached_property
    def _tokenized_name(self):
        toks = list(set(tokenize(self.name)))
        toks.sort()
        return toks

    @cached_property
    def cleaned_name(self):
        clean = [t for t in self._tokenized_name if len(t) > 2 and t not in STOP_WORDS]
        return ' '.join(clean)

    @cached_property
    def cleaned_name_no_type(self):
        clean = [t for t in self._tokenized_name
                 if len(t) > 2 and t not in STOP_WORDS + SCHOOL_TYPES]
        return ' '.join(clean)

    @cached_property
    def types_from_name(self):
        clean = [t for t in self._tokenized_name if t in SCHOOL_TYPES]
        return clean


class School(CleanNameMixIn, models.Model):

    source = models.CharField(max_length=8, blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    local_authority = models.CharField(max_length=255, blank=True, null=True)
    schoolname = models.CharField(max_length=255, blank=True, null=True)
    status_name =  models.CharField(max_length=32, blank=True, null=True)
    postcode = models.CharField(max_length=8, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    phaseofeducation = models.CharField(max_length=32, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    location = models.PointField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'

    @property
    def name(self):
        return self.schoolname

class EducationSite(CleanNameMixIn, models.Model):
    gid = models.IntegerField()
    grid_ref = models.CharField(max_length=2)
    distname = models.CharField(max_length=120, blank=True, null=True)
    sitetheme = models.CharField(max_length=21, blank=True, null=True)
    classifica = models.CharField(max_length=90, blank=True, null=True)
    featcode = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education_site'
        unique_together = (('gid', 'grid_ref'),)

    @property
    def name(self):
        return self.distname


class EducationSiteNearSchool(models.Model):
    site = models.ForeignKey(EducationSite, models.DO_NOTHING, blank=True, null=True)
    school = models.ForeignKey('School', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education_site_near_school'
        unique_together = (('site', 'school'),)


class EducationSiteOverlapsOsm(models.Model):
    site = models.ForeignKey(EducationSite, models.DO_NOTHING, blank=True, null=True)
    ogc_fid = models.ForeignKey('Multipolygons', models.DO_NOTHING, db_column='ogc_fid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'education_site_overlaps_osm'
        unique_together = (('site', 'ogc_fid'),)



class SchoolSite(models.Model):
    school = models.ForeignKey('School', blank=False, null=False)
    site =  models.ForeignKey('EducationSite', blank=False, null=False)

    class Meta:
        unique_together = ('school', 'site')

class Postcodes(models.Model):
    postcode = models.CharField(primary_key=True, max_length=10)
    location = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postcodes'

class ImportLog(models.Model):

    school = models.ForeignKey('School', on_delete=models.PROTECT)
    site =  models.ForeignKey('EducationSite', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    changeset =  models.IntegerField()
    change = models.TextField()


###############################################################
# OpenStreetMap

class Lines(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    wkb_geometry = models.LineStringField(blank=True, null=True)
    osm_id = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    highway = models.CharField(max_length=500, blank=True, null=True)
    waterway = models.CharField(max_length=500, blank=True, null=True)
    aerialway = models.CharField(max_length=500, blank=True, null=True)
    barrier = models.CharField(max_length=500, blank=True, null=True)
    man_made = models.CharField(max_length=500, blank=True, null=True)
    other_tags = HStoreField()

    class Meta:
        managed = False
        db_table = 'lines'


class Multilinestrings(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    wkb_geometry = models.MultiLineStringField(blank=True, null=True)
    osm_id = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    other_tags = HStoreField()

    class Meta:
        managed = False
        db_table = 'multilinestrings'


class Multipolygons(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    wkb_geometry = models.MultiPolygonField(blank=True, null=True)
    osm_id = models.CharField(max_length=500, blank=True, null=True)
    osm_way_id = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    aeroway = models.CharField(max_length=500, blank=True, null=True)
    amenity = models.CharField(max_length=500, blank=True, null=True)
    admin_level = models.CharField(max_length=500, blank=True, null=True)
    barrier = models.CharField(max_length=500, blank=True, null=True)
    boundary = models.CharField(max_length=500, blank=True, null=True)
    building = models.CharField(max_length=500, blank=True, null=True)
    craft = models.CharField(max_length=500, blank=True, null=True)
    geological = models.CharField(max_length=500, blank=True, null=True)
    historic = models.CharField(max_length=500, blank=True, null=True)
    land_area = models.CharField(max_length=500, blank=True, null=True)
    landuse = models.CharField(max_length=500, blank=True, null=True)
    leisure = models.CharField(max_length=500, blank=True, null=True)
    man_made = models.CharField(max_length=500, blank=True, null=True)
    military = models.CharField(max_length=500, blank=True, null=True)
    natural = models.CharField(max_length=500, blank=True, null=True)
    office = models.CharField(max_length=500, blank=True, null=True)
    place = models.CharField(max_length=500, blank=True, null=True)
    shop = models.CharField(max_length=500, blank=True, null=True)
    sport = models.CharField(max_length=500, blank=True, null=True)
    tourism = models.CharField(max_length=500, blank=True, null=True)
    other_tags = HStoreField()

    class Meta:
        managed = False
        db_table = 'multipolygons'


class OtherRelations(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    wkb_geometry = models.GeometryCollectionField(blank=True, null=True)
    osm_id = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    other_tags = HStoreField()

    class Meta:
        managed = False
        db_table = 'other_relations'


class Points(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    wkb_geometry = models.PointField(blank=True, null=True)
    osm_id = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    barrier = models.CharField(max_length=500, blank=True, null=True)
    highway = models.CharField(max_length=500, blank=True, null=True)
    ref = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    is_in = models.CharField(max_length=500, blank=True, null=True)
    place = models.CharField(max_length=500, blank=True, null=True)
    man_made = models.CharField(max_length=500, blank=True, null=True)
    other_tags = HStoreField()

    class Meta:
        managed = False
        db_table = 'points'
