from django.db.models import Q
from django.shortcuts import Http404

from rest_framework import generics, permissions, mixins, filters
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django_geo_db import serializers
from django_geo_db.serializers import LocationSerializer
from django_geo_db.services import GEO_DAL
from django_geo_db.models import Continent, Country, State, Location, City, Zipcode, GeoCoordinate, UserLocation


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
    filter_fields =  ('name', )

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
    filter_fields =  ('continent__continent_id', 'name', 'abbreviation')

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
    filter_fields =  ('country__country_id', 'name')

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
    filter_fields =  ('state__state_id', 'name')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CityDetails(mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer
    filter_fields =  ('country__country_id', 'name', '')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ZipcodeList(mixins.ListModelMixin,
               generics.GenericAPIView):
    queryset = Zipcode.objects.all()
    serializer_class = serializers.ZipcodeSerializer
    filter_fields =  ('zipcode', 'city__city_id')


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

