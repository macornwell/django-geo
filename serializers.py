from rest_framework import serializers
from django_geo.models import Location


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

