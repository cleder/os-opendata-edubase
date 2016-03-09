from __future__ import unicode_literals

#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Edubase(models.Model):
    urn = models.CharField(primary_key=True, max_length=500)
    la_code = models.CharField(max_length=500, blank=True, null=True)
    la_name = models.CharField(max_length=500, blank=True, null=True)
    establishmentnumber = models.CharField(max_length=500, blank=True, null=True)
    establishmentname = models.CharField(max_length=500, blank=True, null=True)
    typeofestablishment_name = models.CharField(max_length=500, blank=True, null=True)
    establishmentstatus_name = models.CharField(max_length=500, blank=True, null=True)
    reasonestablishmentopened_name = models.CharField(max_length=500, blank=True, null=True)
    opendate = models.CharField(max_length=500, blank=True, null=True)
    reasonestablishmentclosed_name = models.CharField(max_length=500, blank=True, null=True)
    closedate = models.CharField(max_length=500, blank=True, null=True)
    phaseofeducation_name = models.CharField(max_length=500, blank=True, null=True)
    statutorylowage = models.CharField(max_length=500, blank=True, null=True)
    statutoryhighage = models.CharField(max_length=500, blank=True, null=True)
    boarders_name = models.CharField(max_length=500, blank=True, null=True)
    officialsixthform_name = models.CharField(max_length=500, blank=True, null=True)
    gender_name = models.CharField(max_length=500, blank=True, null=True)
    religiouscharacter_name = models.CharField(max_length=500, blank=True, null=True)
    diocese_name = models.CharField(max_length=500, blank=True, null=True)
    admissionspolicy_name = models.CharField(max_length=500, blank=True, null=True)
    schoolcapacity = models.CharField(max_length=500, blank=True, null=True)
    specialclasses_name = models.CharField(max_length=500, blank=True, null=True)
    censusdate = models.CharField(max_length=500, blank=True, null=True)
    numberofpupils = models.CharField(max_length=500, blank=True, null=True)
    numberofboys = models.CharField(max_length=500, blank=True, null=True)
    numberofgirls = models.CharField(max_length=500, blank=True, null=True)
    percentagefsm = models.CharField(max_length=500, blank=True, null=True)
    trustschoolflag_name = models.CharField(max_length=500, blank=True, null=True)
    trusts_name = models.CharField(max_length=500, blank=True, null=True)
    schoolsponsorflag_name = models.CharField(max_length=500, blank=True, null=True)
    schoolsponsors_name = models.CharField(max_length=500, blank=True, null=True)
    federationflag_name = models.CharField(max_length=500, blank=True, null=True)
    federations_name = models.CharField(max_length=500, blank=True, null=True)
    ukprn = models.CharField(max_length=500, blank=True, null=True)
    feheidentifier = models.CharField(max_length=500, blank=True, null=True)
    furthereducationtype_name = models.CharField(max_length=500, blank=True, null=True)
    ofstedlastinsp = models.CharField(max_length=500, blank=True, null=True)
    ofstedspecialmeasures_name = models.CharField(max_length=500, blank=True, null=True)
    lastchangeddate = models.CharField(max_length=500, blank=True, null=True)
    street = models.CharField(max_length=500, blank=True, null=True)
    locality = models.CharField(max_length=500, blank=True, null=True)
    address3 = models.CharField(max_length=500, blank=True, null=True)
    town = models.CharField(max_length=500, blank=True, null=True)
    county_name = models.CharField(max_length=500, blank=True, null=True)
    postcode = models.CharField(max_length=500, blank=True, null=True)
    schoolwebsite = models.CharField(max_length=500, blank=True, null=True)
    telephonenum = models.CharField(max_length=500, blank=True, null=True)
    headtitle_name = models.CharField(max_length=500, blank=True, null=True)
    headfirstname = models.CharField(max_length=500, blank=True, null=True)
    headlastname = models.CharField(max_length=500, blank=True, null=True)
    headhonours = models.CharField(max_length=500, blank=True, null=True)
    headpreferredjobtitle = models.CharField(max_length=500, blank=True, null=True)
    teenmoth_name = models.CharField(max_length=500, blank=True, null=True)
    teenmothplaces = models.CharField(max_length=500, blank=True, null=True)
    ccf_name = models.CharField(max_length=500, blank=True, null=True)
    senpru_name = models.CharField(max_length=500, blank=True, null=True)
    ebd_name = models.CharField(max_length=500, blank=True, null=True)
    ftprov_name = models.CharField(max_length=500, blank=True, null=True)
    edbyother_name = models.CharField(max_length=500, blank=True, null=True)
    section41approved_name = models.CharField(max_length=500, blank=True, null=True)
    sen1_name = models.CharField(max_length=500, blank=True, null=True)
    sen2_name = models.CharField(max_length=500, blank=True, null=True)
    sen3_name = models.CharField(max_length=500, blank=True, null=True)
    gor_name = models.CharField(max_length=500, blank=True, null=True)
    administrativeward_name = models.CharField(max_length=500, blank=True, null=True)
    parliamentaryconstituency_name = models.CharField(max_length=500, blank=True, null=True)
    urbanrural_name = models.CharField(max_length=500, blank=True, null=True)
    gsslacode_name = models.CharField(max_length=500, blank=True, null=True)
    easting = models.CharField(max_length=500, blank=True, null=True)
    northing = models.CharField(max_length=500, blank=True, null=True)
    msoa_name = models.CharField(max_length=500, blank=True, null=True)
    lsoa_name = models.CharField(max_length=500, blank=True, null=True)
    boardingestablishment_name = models.CharField(max_length=500, blank=True, null=True)
    previousla_code = models.CharField(max_length=500, blank=True, null=True)
    previousla_name = models.CharField(max_length=500, blank=True, null=True)
    previousestablishmentnumber = models.CharField(max_length=500, blank=True, null=True)
    location = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'edubase'


class FunctionalSite(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.CharField(max_length=38, blank=True, null=True)
    distname = models.CharField(max_length=120, blank=True, null=True)
    sitetheme = models.CharField(max_length=21, blank=True, null=True)
    classifica = models.CharField(max_length=90, blank=True, null=True)
    featcode = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'functional_site'


class Postcodes(models.Model):
    postcode = models.CharField(primary_key=True, max_length=10)
    location = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postcodes'



class SeedData(models.Model):
    seedcode = models.CharField(max_length=200, blank=True, null=True)
    laname = models.CharField(max_length=200, blank=True, null=True)
    centretype = models.CharField(max_length=200, blank=True, null=True)
    schoolname = models.CharField(max_length=200, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    address3 = models.CharField(max_length=200, blank=True, null=True)
    postcode = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    primary_school = models.CharField(max_length=200, blank=True, null=True)
    secondary = models.CharField(max_length=200, blank=True, null=True)
    special = models.CharField(max_length=200, blank=True, null=True)
    primaryroll = models.CharField(max_length=200, blank=True, null=True)
    secondaryroll = models.CharField(max_length=200, blank=True, null=True)
    specialroll = models.CharField(max_length=200, blank=True, null=True)
    primary1 = models.CharField(max_length=200, blank=True, null=True)
    secondary1 = models.CharField(max_length=200, blank=True, null=True)
    special1 = models.CharField(max_length=200, blank=True, null=True)
    denomination = models.CharField(max_length=200, blank=True, null=True)
    location = models.GeometryField(geography=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seed_data'


class EdubaseSite(models.Model):
    school = models.ForeignKey('Edubase', blank=False, null=False)
    site =  models.ForeignKey('FunctionalSite', blank=False, null=False)

class SeedSite(models.Model):
    school = models.ForeignKey('SeedData', blank=False, null=False)
    site =  models.ForeignKey('FunctionalSite', blank=False, null=False)
