# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import openfruit.common.models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('generated_name', models.CharField(null=True, max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('continent_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('abbreviation', models.CharField(max_length=2, unique=True)),
                ('continent', models.ForeignKey(to='geography.Continent')),
            ],
        ),
        migrations.CreateModel(
            name='GeoCoordinate',
            fields=[
                ('geocoordinate_id', models.AutoField(serialize=False, primary_key=True)),
                ('lat', models.DecimalField(decimal_places=5, max_digits=7)),
                ('lon', models.DecimalField(decimal_places=5, max_digits=8)),
                ('generated_name', models.CharField(null=True, max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(null=True, max_length=30, blank=True)),
                ('generated_name', models.CharField(null=True, max_length=50, blank=True)),
                ('city', models.ForeignKey(null=True, to='geography.City', blank=True)),
                ('country', models.ForeignKey(to='geography.Country')),
                ('geocoordinate', models.ForeignKey(null=True, to='geography.GeoCoordinate', help_text='This is a very specific location.', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('abbreviation', models.CharField(max_length=2, unique=True)),
                ('generated_name', models.CharField(null=True, max_length=50, blank=True)),
                ('country', models.ForeignKey(to='geography.Country')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
            ],
        ),
        migrations.CreateModel(
            name='UserGeographySettings',
            fields=[
                ('user_geography_settings_id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.ForeignKey(to='geography.Location')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('user_location_id', models.AutoField(serialize=False, primary_key=True)),
                ('last_used', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('location', models.ForeignKey(to='geography.Location')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('last_used',),
            },
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('zipcode_id', models.AutoField(serialize=False, primary_key=True)),
                ('zipcode', openfruit.common.models.IntegerRangeField(unique=True)),
                ('timezone', models.IntegerField()),
                ('generated_name', models.CharField(null=True, max_length=50, blank=True)),
                ('city', models.ForeignKey(to='geography.City')),
                ('geocoordinate', models.ForeignKey(to='geography.GeoCoordinate')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(null=True, to='geography.State', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='zipcode',
            field=models.ForeignKey(null=True, to='geography.Zipcode', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='geocoordinate',
            unique_together=set([('lat', 'lon')]),
        ),
        migrations.AddField(
            model_name='country',
            name='geocoordinate',
            field=models.ForeignKey(to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='city',
            name='geocoordinate',
            field=models.ForeignKey(to='geography.GeoCoordinate'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='geography.State'),
        ),
        migrations.AlterUniqueTogether(
            name='zipcode',
            unique_together=set([('zipcode', 'geocoordinate')]),
        ),
        migrations.AlterUniqueTogether(
            name='userlocation',
            unique_together=set([('user', 'location')]),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('country', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('country', 'state', 'city', 'zipcode', 'geocoordinate')]),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('state', 'name')]),
        ),
    ]
