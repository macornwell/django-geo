# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-20 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_geo_db', '0011_auto_20180314_0254'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateRegion',
            fields=[
                ('state_region_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('counties', models.ManyToManyField(to='django_geo_db.County')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.State')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='stateregion',
            unique_together=set([('state', 'name')]),
        ),
    ]