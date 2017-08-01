import os
import csv
from django_geo_db.models import UserLocation, Zipcode, Location

US_CITIES_FILE = 'us-cities-and-zips.csv'
US_STATES_FILE = 'us-states.csv'
COUNTRIES_FILE = 'countries.csv'

class GeographyDAL:

    def get_all_named_locations(self, include_private=False):
        objects = Location.objects.filter(name__isnull=False)
        if not include_private:
            objects = objects.filter(is_private=False)
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
        reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
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
    file_path = os.path.join(module_dir, US_STATES_FILE)
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
    (zip_code,latitude,longitude,city,state, timezone)
    :return:
    """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, US_CITIES_FILE)
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            state = row['state'].strip()
            city = row['city'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            zip = row['zip'].strip()
            timezone = row['timezone']
            yield (zip, lat, lon, city, state, timezone)


def generate_countries():
    """
    Iterates through a list of all of the US cities.
    (country name, continent,abbreviation,latitude,longitude)
    :return:
    """
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, COUNTRIES_FILE)
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            abbr = row['abbreviation'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            country = row['name'].strip().replace('"', '')
            continent = row['continent'].strip()
            yield (country, continent, abbr, lat, lon)
