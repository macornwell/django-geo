import io
from django.conf import settings
from django.shortcuts import Http404, HttpResponse
from wsgiref.util import FileWrapper
from rest_framework import permissions, mixins, filters, generics, status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django_geo_db import serializers
from django_geo_db.serializers import LocationSerializer, LocationMapTypeSerializer, LocationMapSerializer
from django_geo_db.services import GEO_DAL, LocationMapGenerator
from django_geo_db.models import Continent, Country, State, Location, City, \
    Zipcode, GeoCoordinate, UserLocation, County, LocationMapType, LocationMap, LocationBounds, StateRegion
from django_geo_db.storage import DataStorage
from django_geo_db.utilities import MarkedMap, LatLon


class LocationDetail(APIView):
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LocationSerializer(snippet, context={'request': request})
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


class CountyList(mixins.ListModelMixin,
                 generics.GenericAPIView):
    queryset = County.objects.all()
    serializer_class = serializers.CountrySerializer
    filter_fields =  ('state__state_id', 'name'),

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CountyDetails(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    queryset = County.objects.all()
    serializer_class = serializers.CountySerializer

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


class StateRegionList(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = StateRegion.objects.all()
    serializer_class = serializers.StateRegionSerializer
    filter_fields = ('name', 'state_id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StateRegionDetails(mixins.RetrieveModelMixin,
                         generics.GenericAPIView):
    queryset = StateRegion.objects.all()
    serializer_class = serializers.StateRegionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class LocationMapView(APIView):
    """
    Queries for LocationMap objects.

    Possible Queries:
    /location-map/?type=simple&country=United States of America
    /location-map/?type=simple&country=United States of America
    /location-map/?type=simple&country=United States of America&state=California
    /location-map/?type=simple&country=United States of America&state=California&county=San Diego
    /location-map/?type=simple&country=United States of America&state=California&city=San Diego
    /location-map/?type=simple&country=United States of America&state=California&county=San Diego&city=San Diego
    /location-map/?type=simple&country=United States of America&state=California&county=San Diego&city=San Diego&zipcode=91932
    /location-map/?type=simple&country=United States of America&zipcode=91932
    /location-map/?type=simple&country=United States of America&region=Appalachia
    /location-map/?type=simple&country=United States of America&state=Indiana&name=Throckmorton-Purdue Agricultural Center

    Example Request:
    /location-map/?country=United States of America&state=California&city=San Diego

    Example Result
    {
        "type": "http://localhost:8000/location-map-type/1/",
        "map_file_url": "http://localhost:8000/media/django_geo_db/maps/simple/united-states-of-america/alabama-brewton.png",
        "location": "http://localhost:8000/location/160403/"
    }

    """

    def __validate_query_params(self, country, state, county, city, zipcode, map_type):
        if not country:
            return 'Must include country in request.'
        if county and not state:
            return 'Must have state with a county request.'
        if city and not state:
            return 'Must have state with a city request.'
        if not map_type:
            return 'No Map Type provided.'

    def post(self, request):
        map_type = request.query_params.get('type', None)
        country = request.query_params.get('country', None)
        state = request.query_params.get('state', None)
        county = request.query_params.get('county', None)
        city = request.query_params.get('city', None)
        zipcode = request.query_params.get('zipcode', None)
        region = request.query_params.get('region', None)
        name = request.query_params.get('name', None)
        error_message = self.__validate_query_params(country, state, county, city, zipcode, map_type)
        if error_message:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        map_type = GEO_DAL.get_map_type(map_type)
        domain = request.build_absolute_uri('/')[0:-1]
        if region:
            location = GEO_DAL.get_region(country, name)
            location_map = LocationMapGenerator(domain).get_regional_map(map_type, location)
        else:
            location = GEO_DAL.get_location(country, state, county, city, zipcode, name)
            location_map = LocationMapGenerator(domain).get_or_generate_location_map(map_type, location)
        if not location:
            return Response({'error': 'Location was not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LocationMapSerializer(location_map, context={'request': request})
        data = serializer.data
        url = data['map_file_url']
        if 'static' not in url:
            data['map_file_url'] = request.build_absolute_uri(settings.MEDIA_URL + data['map_file_url'])
        return Response(data)


class LocationMapTypeDetail(APIView):
    def get_object(self, pk):
        try:
            return LocationMapType.objects.get(pk=pk)
        except LocationMapType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LocationMapTypeSerializer(snippet)
        return Response(serializer.data)


class PlotMap(APIView):
    """
    Plots markers on a map.

    Examples:
    /plot/simple/country/united-states-of-america/united-states-of-america/&marker=star&size_percent=0.05

    Body Params:
    ll_1=30.1235 -90.1234&ll_2=30.1545 -90.15123

    """

    def post(self, request, map_type, location_type, country_name, location_name):
        domain = request.build_absolute_uri('/')[0:-1]

        country_name = country_name.replace('-', ' ')
        obj = location_name.replace('-', ' ')
        country_obj = Country.objects.get(name__iexact=country_name)
        location = None
        if location_type == 'country':
            location = Location.objects.get(country=country_obj, state=None, region=None, name=None)
        elif location_type == 'region':
            location = Location.objects.get(country=country_obj, state=None, region__name__iexact=obj, name=None)
        elif location_type == 'state':
            location = Location.objects.get(country=country_obj, state__name__iexact=obj,
                                            region=None, name=None, county=None, zipcode=None, city=None)
        bounds = LocationBounds.objects.get(location=location)

        map_type = LocationMapType.objects.get(type=map_type)
        location_type = LocationMap.objects.get(location=location, type=map_type)

        storage = DataStorage(domain)
        map_data = storage.get_static_or_media_data(location_type.map_file_url)

        marker = request.query_params.get('marker', 'star')
        size_percent = float(request.query_params.get('size_percent', 0.05))
        coords = [LatLon.parse_string(request.POST[p]) for p in request.POST if p.startswith('ll_')]
        marked_map = MarkedMap(storage, map_data, bounds)

        markers = {
            'star': 'add_star_to_base_map',
        }

        combined = map_data
        for coord in coords:
            method_name = markers[marker]
            combined = getattr(marked_map, method_name)(coord, marker_size=size_percent).getvalue()
            # Recreate the object to use the updated map because we're adding many marks to it.
            marked_map = MarkedMap(storage, combined, bounds)

        wrapper = FileWrapper(io.BytesIO(combined))
        response = HttpResponse(wrapper, content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="map.png"'
        return response


