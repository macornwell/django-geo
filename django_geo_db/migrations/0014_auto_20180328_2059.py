# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-28 20:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_geo_db', '0013_auto_20180321_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='CeleryPlottedMapTask',
            fields=[
                ('celery_plotted_map_task_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_submitted', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('p', 'Pending'), ('t', 'Started'), ('r', 'Retry'), ('f', 'Failure'), ('s', 'Success')], max_length=1)),
                ('task_id', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlottedMap',
            fields=[
                ('plotted_map_id', models.AutoField(primary_key=True, serialize=False)),
                ('map_file_url', models.URLField(blank=True, null=True)),
                ('marker_type', models.CharField(max_length=20)),
                ('marker_size', models.DecimalField(decimal_places=2, max_digits=3)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.Location')),
                ('location_map_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.LocationMapType')),
            ],
        ),
        migrations.AddField(
            model_name='celeryplottedmaptask',
            name='plotted_map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.PlottedMap'),
        ),
    ]
