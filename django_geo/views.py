from django.db.models import Q
from django.shortcuts import Http404
from dal import autocomplete

from rest_framework import generics, permissions, mixins
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django_geo import serializers
from django_geo.serializers import LocationSerializer
from django_geo.services import GEO_DAL
from django_geo.models import Continent, Country, State, Location, City, Zipcode, GeoCoordinate, UserLocation


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


class LocationDetail(APIView):
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LocationSerializer(snippet)
        return Response(serializer.data)


class LocationList(generics.ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        return GEO_DAL.get_all_named_locations()


class ContinentList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = Continent.objects.all()
    serializer_class = serializers.ContinentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ContinentDetails(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    queryset = Continent.objects.all()
    serializer_class = serializers.ContinentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CountryList(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CountryDetails(mixins.RetrieveModelMixin,
                       generics.GenericAPIView):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class StateList(mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StateDetails(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CityList(mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CityDetails(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ZipcodeList(mixins.ListModelMixin,
               generics.GenericAPIView):
    queryset = Zipcode.objects.all()
    serializer_class = serializers.ZipcodeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ZipcodeDetails(mixins.RetrieveModelMixin,
                  generics.GenericAPIView):
    queryset = Zipcode.objects.all()
    serializer_class = serializers.ZipcodeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GeoCoordinateList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = GeoCoordinate.objects.all()
    serializer_class = serializers.GeoCoordinateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GeoCoordinateDetails(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    queryset = GeoCoordinate.objects.all()
    serializer_class = serializers.GeoCoordinateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
