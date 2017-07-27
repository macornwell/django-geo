from rest_framework import serializers
from django_geo.models import Location, GeoCoordinate, Zipcode, Continent, Country, State, City


class GeoCoordinateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeoCoordinate
        fields = ('geocoordinate_id', 'lat', 'lon', 'generated_name')


class ContinentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Continent
        fields = ('continent_id', 'name')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('country_id', 'continent', 'name', 'abbreviation', 'geocoordinate')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = State
        fields = ('state_id', 'country', 'name', 'abbreviation', 'geocoordinate', 'generated_name')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('city_id', 'state', 'name', 'geocoordinate', 'generated_name')


class ZipcodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zipcode
        fields = ('zipcode_id', 'city', 'zipcode', 'geocoordinate', 'timezone')


class LocationSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()

    def get_lat(self, obj):
        return str(obj.geocoordinate.lat)

    def get_lon(self, obj):
        return str(obj.geocoordinate.lon)

    class Meta:
        model = Location
        fields = ('location_id', 'country', 'city', 'zipcode', 'geocoordinate', 'lat', 'lon', 'name', 'generated_name')

