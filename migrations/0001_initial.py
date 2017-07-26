# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('city_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=8, null=True, blank=True)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=8, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('continent_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('continent', models.ForeignKey(to='geography.Continent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('location', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=8, null=True, blank=True)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=8, null=True, blank=True)),
                ('city', models.ForeignKey(null=True, to='geography.City', blank=True)),
                ('country', models.ForeignKey(to='geography.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('state_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(to='geography.Country')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(to='geography.State'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='geography.State'),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together=set([('country', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('state', 'name')]),
        ),
    ]
