from django.db.models import Q
from django.shortcuts import Http404
from dal import autocomplete

from rest_framework import generics, permissions, mixins, filters
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django_geo_db import serializers
from django_geo_db.serializers import LocationSerializer
from django_geo_db.services import GEO_DAL
from django_geo_db.models import Continent, Country, State, Location, City, Zipcode, GeoCoordinate, UserLocation


class UsersLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Location.objects.none()

        user = self.request.user
        qs = UserLocation.objects.filter(user=user)

        if self.q:
            qs = qs.filter(
                Q(location__generated_name__icontains=self.q),
            )
        return qs


class NamedLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Location.objects.none()

        qs = Location.objects.filter(name__isnull=False)

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q)
            )
        return qs


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Location.objects.none()

        qs = Location.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q) |
                Q(generated_name__endswith=self.q)
            )
        return qs


class PublicLocationsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Location.objects.public_locations()

        if self.q:
            qs = qs.filter(
                Q(generated_name__contains=self.q)
            )
        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return City.objects.none()

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q) |
                Q(generated_name__endswith=self.q)
            )
        return qs


class ZipcodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Zipcode.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__iendswith=self.q)
            )
        return qs


class GeoCoordinateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return GeoCoordinate.objects.none()

        qs = GeoCoordinate.objects.all()

        if self.q:
            qs = qs.filter(
                Q(generated_name__istartswith=self.q)
            )
        return qs

