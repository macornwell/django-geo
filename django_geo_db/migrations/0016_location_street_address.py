# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-22 23:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_geo_db', '0015_auto_20181022_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]