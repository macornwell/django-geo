from django.db import models
from django_geo_db.utilities import get_lat_lon_from_string

class GeoCoordinateManager(models.Manager):

    def get_or_create_by_lat_lon(self, lat, lon):
        lat, lon = get_lat_lon_from_string('{0} {1}'.format(lat, lon))
        return super(GeoCoordinateManager, self).get_or_create(lat=lat, lon=lon)


class LocationManager(models.Manager):

    def public_locations(self):
        return super(LocationManager, self).filter(name__isnull=False, is_private=False)
