# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 17:20
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import schools.models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_edubasesite_seedsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=8, null=True)),
                ('uid', models.IntegerField(blank=True, null=True)),
                ('local_authority', models.CharField(blank=True, max_length=255, null=True)),
                ('schoolname', models.CharField(blank=True, max_length=255, null=True)),
                ('status_name', models.CharField(blank=True, max_length=32, null=True)),
                ('postcode', models.CharField(blank=True, max_length=8, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('locality', models.CharField(blank=True, max_length=255, null=True)),
                ('town', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=32, null=True)),
                ('phaseofeducation', models.CharField(blank=True, max_length=32, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'school',
                'managed': False,
            },
            bases=(schools.models.CleanNameMixIn, models.Model),
        ),
    ]
