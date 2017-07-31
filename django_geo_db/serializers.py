from rest_framework import serializers
from django_geo_db.models import Location, GeoCoordinate, Zipcode, Continent, Country, State, City


class GeoCoordinateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('geocoordinate-detail')
    class Meta:
        model = GeoCoordinate
        fields = ('geocoordinate_id', 'lat', 'lon', 'generated_name', 'url')


class ContinentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('continent-detail')
    class Meta:
        model = Continent
        fields = ('continent_id', 'name', 'url')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('country-detail')
    class Meta:
        model = Country
        fields = ('country_id', 'continent', 'name', 'abbreviation', 'geocoordinate', 'url')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('state-detail')
    class Meta:
        model = State
        fields = ('state_id', 'country', 'name', 'abbreviation', 'geocoordinate', 'generated_name', 'url')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('city-detail')
    class Meta:
        model = City
        fields = ('city_id', 'state', 'name', 'geocoordinate', 'generated_name', 'url')


class ZipcodeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('zipcode-detail')
    class Meta:
        model = Zipcode
        fields = ('zipcode_id', 'city', 'zipcode', 'geocoordinate', 'timezone', 'url')


class LocationSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField('location-detail')

    def get_lat(self, obj):
        return str(obj.geocoordinate.lat)

    def get_lon(self, obj):
        return str(obj.geocoordinate.lon)

    class Meta:
        model = Location
        fields = ('location_id', 'country', 'city', 'zipcode', 'geocoordinate', 'lat', 'lon', 'name', 'generated_name', 'url')

