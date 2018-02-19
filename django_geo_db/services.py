import os
import csv
from django_geo_db.models import UserLocation, Zipcode, Location, Country, State

US_CITIES_FILE = 'us-data-final.csv'
US_STATES_FILE = 'us-states.csv'
COUNTRIES_FILE = 'countries.csv'

class GeographyDAL:

    def get_us_country(self):
        return Country.objects.get(name='United States of America')

    def get_us_states(self):
        return State.objects.filter(country=self.get_us_country()).order_by('name')

    def get_country_by_name(self, name):
        country = Country.objects.filter(name__iexact=name).first()
        return country

    def get_all_named_locations(self, include_private=False):
        objects = Location.objects.filter(name__isnull=False)
        return objects

    def get_location_by_id(self, id):
        return Location.objects.get(pk=id)

    def get_users_locations(self, user):
        return UserLocation.objects.filter(user=user).values_list('location', flat=True)

    def append_user_location(self, user, locationUsedByUser):
        obj, created = UserLocation.objects.get_or_create(user=user, location=locationUsedByUser)
        if not created:
            obj.save()  # This triggers the updating of the date.

    def get_zipcode_by_zip(self, zipcode):
        return Zipcode.objects.get(zipcode=zipcode)

    def create_location(self, zipcode, coordinate, name):
        city = zipcode.city
        state = city.state
        country = state.country
        location, created = Location.objects.get_or_create(country=country, state=state, city=city, zipcode=zipcode, geocoordinate=coordinate, name=name)
        return location

    def geocode_zipcode_from_lat_lon(self, lat, lon):
        """
        Only use this method if you have googlemaps installed.
        """
        import googlemaps
        from django.conf import settings
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
        zipcodeObj = None
        for index in range(0, len(reverse_geocode_result[0]['address_components'])):
            obj = reverse_geocode_result[0]['address_components']
            if obj[index]['types'][0] == 'postal_code':
                zipcode = obj[index]['short_name']
                zipcodeObj = Zipcode.objects.get(zipcode=zipcode)
                break
        return zipcodeObj

GEO_DAL = GeographyDAL()


def generate_current_us_states_list():
    """
    Iterates through a list of all of the US States.
    (state, abbreviation, latitude, longitude)
    :return:
    """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data', US_STATES_FILE)
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row['state'].strip()
            abbreviation = row['abbreviation'].strip()
            latitude = row['latitude'].strip()
            longitude = row['longitude'].strip()
            yield (state, abbreviation, latitude, longitude)


def generate_current_us_cities_list():
    """
    Iterates through a list of all of the US cities.
    (zip,city,state,county,latitude,longitude,timezone,dst)
    :return:
    """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data', US_CITIES_FILE)
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row['state'].strip()
            county = row['county'].strip()
            city = row['city'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            zip = row['zip'].strip()
            timezone = row['timezone']
            yield (zip, lat, lon, city, county, state, timezone)


def generate_countries():
    """
    Iterates through a list of all of the US cities.
    (country name, continent,abbreviation,latitude,longitude)
    :return:
    """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data', COUNTRIES_FILE)
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            abbr = row['abbreviation'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            country = row['name'].strip().replace('"', '')
            continent = row['continent'].strip()
            yield (country, continent, abbr, lat, lon)
