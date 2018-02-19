from decimal import Decimal
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django_geo_db.managers import GeoCoordinateManager
from django_geo_db.utilities import get_standardized_coordinate


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class GeoCoordinate(models.Model):
    objects = GeoCoordinateManager()
    geocoordinate_id = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=7, decimal_places=5)
    lon = models.DecimalField(max_digits=8, decimal_places=5)
    generated_name = models.CharField(max_length=50, blank=True, null=True)

    lat_neg = models.BooleanField(default=False)
    lat_tens = IntegerRangeField(min_value=-9, max_value=9, blank=True, null=True)
    lat_ones = IntegerRangeField(min_value=0, max_value=9, blank=True, null=True)
    lat_tenths = IntegerRangeField(min_value=0, max_value=9, blank=True, null=True)
    lat_hundredths = IntegerRangeField(min_value=0, max_value=9, blank=True, null=True)
    lat_thousands = IntegerRangeField(min_value=-0, max_value=9, blank=True, null=True)

    lon_neg = models.BooleanField(default=False)
    lon_hundreds = IntegerRangeField(min_value=-9, max_value=9, blank=True, null=True)
    lon_tens = IntegerRangeField(min_value=-0, max_value=9, blank=True, null=True)
    lon_ones = IntegerRangeField(min_value=0, max_value=9, blank=True, null=True)
    lon_tenths = IntegerRangeField(min_value=0, max_value=9, blank=True, null=True)
    lon_hundredths = IntegerRangeField(min_value=0, max_value=9, blank=True, null=True)
    lon_thousands = IntegerRangeField(min_value=-0, max_value=9, blank=True, null=True)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def save(self, *args, **kwargs):
        self.__standardize_fractionals()
        self.generated_name = self.__get_generated_name()
        self.__generate_whole_fractionals()
        super(GeoCoordinate, self).save(*args, **kwargs)

    def __get_generated_name(self):
        return '{0} {1}'.format(self.lat, self.lon)

    def __standardize_fractionals(self):
        self.lat = get_standardized_coordinate(self.lat)
        self.lon = get_standardized_coordinate(self.lon)

    def __generate_whole_fractionals(self):
        try:
            self.lat_neg, self.lat_tens, self.lat_ones, self.lat_tenths, self.lat_hundredths, self.lat_thousands, other, other2 = GeoCoordinate.split_lat_coordinate(self.lat)
        except:
            message = '{0} {1}'.format(self.lat, GeoCoordinate.split_lat_coordinate(self.lat))
            raise Exception(message)
        try:
            self.lon_neg, self.lon_hundreds, self.lon_tens, self.lon_ones, self.lon_tenths, self.lon_hundredths, self.lon_thousands, other, other2 = GeoCoordinate.split_lon_coordinate(self.lon)
        except:
            message = '{0} {1}'.format(self.lon, GeoCoordinate.split_lon_coordinate(self.lon))
            raise Exception(message)

    @staticmethod
    def __split_frac(frac):
        coord_points = []
        for i in range(0, len(frac)):
            coord_points.append(int(frac[i]))
        return coord_points

    @staticmethod
    def split_lat_coordinate(coordinate):
        coord_points = []
        whole, frac = str(coordinate).split('.', 1)
        is_negative = whole[0] is '-'
        if is_negative:
            whole = whole[1:]
            coord_points.append(True)
        else:
            coord_points.append(False)
        whole = '{0:02d}'.format(int(whole))
        if whole[0] == '0':
            coord_points.append(0)
            coord_points.append(int(whole[1]))
        else:
            coord_points.append(int(whole[0]))
            coord_points.append(int(whole[1]))
        coord_points += GeoCoordinate.__split_frac(frac)
        zeros_to_add = 8 - len(coord_points)
        for i in range(0, zeros_to_add):
            coord_points.append(0)
        return coord_points

    @staticmethod
    def split_lon_coordinate(coordinate):
        coord_points = []
        whole, frac = str(coordinate).split('.', 1)
        is_negative = whole[0] is '-'
        if is_negative:
            whole = whole[1:]
            coord_points.append(True)
        else:
            coord_points.append(False)
        whole = '{0:03d}'.format(int(whole))
        if whole[0] == '0':
            coord_points.append(0)
            if whole[1] == '0':
                coord_points.append(0)
            else:
                coord_points.append(int(whole[1]))
            coord_points.append(int(whole[2]))
        else:
            coord_points.append(int(whole[0]))
            coord_points.append(int(whole[1]))
            coord_points.append(int(whole[2]))
        coord_points += GeoCoordinate.__split_frac(frac)
        zeros_to_add = 9 - len(coord_points)
        for i in range(0, zeros_to_add):
            coord_points.append(0)
        return coord_points


    class Meta:
        unique_together = ('lat', 'lon')


class Continent(models.Model):
    continent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    continent = models.ForeignKey(Continent)
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=2, unique=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)

    def __str__(self):
        return self.name


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=2, unique=True)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    generated_name = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.generated_name = self.__get_generated_name()
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def __get_generated_name(self):
        return str('{0}, {1}'.format(self.name, self.country.abbreviation))

    class Meta:
        unique_together = (('country', 'name'),)


class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State)
    name = models.CharField(max_length=50)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    generated_name = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.generated_name = self.__get_generated_name()
        return super(County, self).save(*args, **kwargs)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def __get_generated_name(self):
        return str('{0}, {1}'.format(self.name, self.state.abbreviation))

    class Meta:
        unique_together = (('state', 'name'),)


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State)
    county = models.ForeignKey(County, blank=True, null=True)
    name = models.CharField(max_length=50)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    generated_name = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.generated_name = self.__get_generated_name()
        return super(City, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('state', 'name', 'county'),)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def __get_generated_name(self):
        return str('{0}, {1}'.format(self.name, self.state.name))


class Zipcode(models.Model):
    zipcode_id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City)
    zipcode = IntegerRangeField(unique=True, min_value=1, max_value=99999)
    geocoordinate = models.ForeignKey(GeoCoordinate)
    timezone = models.IntegerField()
    generated_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('zipcode', 'geocoordinate')

    def save(self, *args, **kwargs):
        self.generated_name = self.__get_generated_name()
        return super(Zipcode, self).save(*args, **kwargs)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def __get_generated_name(self):
        return str('{0}, {1} {2}'.format(self.city.name, self.city.state.name, self.zipcode))


class Location(models.Model):
    """
    The working horse of locational data.
    This is the object that should be a foreign key to MOST geolocated objects.
    It is a cascading of Locational information that gets more detailed depending on
    what level of granularity is desired, the minimum being a country.
    """
    location_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State, blank=True, null=True)
    county = models.ForeignKey(County, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    zipcode = models.ForeignKey(Zipcode, blank=True, null=True)
    geocoordinate = models.ForeignKey(GeoCoordinate, blank=True, null=True, help_text='This is a very specific location.')
    name = models.CharField(max_length=30, blank=True, null=True)
    generated_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.generated_name or self.__get_generated_name()

    def get_geocoordinate(self):
        """
        Gets the most specific geocoordinate for this Location.
        :return:
        """
        if self.geocoordinate:
            return self.geocoordinate
        obj = self.zipcode
        if not obj:
            obj = self.city
        if not obj:
            obj = self.county
        if not obj:
            obj = self.state
        if not obj:
            obj = self.country
        return obj.geocoordinate

    def lat(self):
        return self.get_geocoordinate().lat

    def lon(self):
        return self.get_geocoordinate().lon

    def lat_lon(self):
        return str(self.get_geocoordinate())

    def save(self, *args, **kwargs):
        self.__set_cascading_details()
        self.__set_generated_name()
        self.__validate_interconnection_details()
        return super(Location, self).save(*args, **kwargs)

    def __set_cascading_details(self):
        if self.zipcode and not self.city:
            self.city = self.zipcode.city
        if self.city and not self.county:
            self.county = self.city.county
        if self.county and not self.state:
            self.state = self.county.state
        if self.state and not self.country:
            self.country = self.state.country

    def __validate_interconnection_details(self):
        if self.state and self.state.country != self.country:
            raise Exception("The state's country does not match the selected country.")
        if self.city and self.city.county != self.county:
            raise Exception("City's state does not match the selected state.")
        if self.zipcode and self.zipcode.city != self.city:
            raise Exception("Zipcode's city does not match the selected city.")
        if self.county and self.county.state != self.state:
            raise Exception('County does not match the selected state')
        if self.name and not self.geocoordinate:
            raise Exception('Names must have a geocoordinate.')
        if not self.name and self.geocoordinate:
            raise Exception('Geocoordinates must be named.')

    def __set_generated_name(self):
        self.generated_name = self.__get_generated_name()

    def __get_generated_name(self):
        value = ''
        if self.name:
            value = '{0} ({1})'.format(self.name, self.geocoordinate)
        elif self.zipcode:
            value = '{0}, {1} {2}'.format(self.city.name, self.state.abbreviation, self.zipcode.zipcode)
        elif self.city:
            value = '{0}, {1}'.format(self.city.name, self.state.abbreviation)
        elif self.state:
            value = '{0}, {1}'.format(self.state.name, self.country.name)
        else:
            value = '{0}'.format(self.country.name)
        return value

    class Meta:
        unique_together = ('country', 'state', 'city', 'zipcode', 'geocoordinate')


class GeographicRegion(models.Model):
    """
    An "informal" regional area that encompasses a number of locations.
    """
    geographic_region_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    locations = models.ManyToManyField(Location)


class UserLocation(models.Model):
    """
    A location that a user has used in the past.
    """
    user_location_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    last_used = models.DateTimeField(default=datetime.now, blank=True)
    user_created = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.last_used = datetime.now()
        return super(UserLocation, self).save(args, kwargs)

    def __str__(self):
        return self.location.name

    class Meta:
        ordering = ('last_used',)
        unique_together = ('user', 'location')


