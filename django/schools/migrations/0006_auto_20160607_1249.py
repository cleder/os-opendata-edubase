# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-07 12:49
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0005_add_importlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.IntegerField()),
                ('grid_ref', models.CharField(max_length=2)),
                ('distname', models.CharField(blank=True, max_length=120, null=True)),
                ('sitetheme', models.CharField(blank=True, max_length=21, null=True)),
                ('classifica', models.CharField(blank=True, max_length=90, null=True)),
                ('featcode', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'education_site',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EducationSiteNearSchool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'education_site_near_school',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EducationSiteOverlapsOsm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'education_site_overlaps_osm',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='importlog',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='schools.EducationSite'),
        ),
        migrations.AlterField(
            model_name='schoolsite',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.EducationSite'),
        ),
    ]