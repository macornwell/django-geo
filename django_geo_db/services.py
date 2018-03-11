import os, io
import csv
import json
import urllib.request

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.files.storage import default_storage

from PIL import Image

from django_geo_db.utilities import BoundingBoxAndMap
from django_geo_db.math import Translations
from django_geo_db.models import UserLocation, Zipcode, Location, Country, \
    State, LocationMap, LocationBounds, LocationMapType
import os


MAP_STAR_PERCENTAGE = 0.05
US_CITIES_FILE = 'us-data-final.csv'
US_STATES_FILE = 'us-states.csv'
COUNTRIES_FILE = 'countries.csv'
US_STATES_BOUNDS_FILE = 'us-state-boundaries.json'


class GeographyDAL:

    def get_map_type(self, map_type):
        return LocationMapType.objects.get(type=map_type)

    def get_location(self, country_name, state_name=None, county_name=None, city_name=None, zipcode=None):
        result = Location.objects.filter(country__name__iexact=country_name)
        if zipcode:
            result = result.filter(zipcode__zipcode=zipcode).first()
            return result
        if state_name:
            result = result.filter(state__name__iexact=state_name)
        if county_name:
            result = result.filter(county__name__iexact=county_name)
        if city_name:
            result = result.filter(city__name__iexact=city_name)
        return result.first()

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


def get_data_file(filename):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data', filename)
    return file_path


def generate_current_us_states_list():
    """
    Iterates through a list of all of the US States.
    (state, abbreviation, latitude, longitude)
    :return:
    """
    file_path = get_data_file(US_STATES_FILE)
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
    file_path = get_data_file(US_CITIES_FILE)
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
    file_path = get_data_file(COUNTRIES_FILE)
    with open(file_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            abbr = row['abbreviation'].strip()
            lat = row['latitude'].strip()
            lon = row['longitude'].strip()
            country = row['name'].strip().replace('"', '')
            continent = row['continent'].strip()
            yield (country, continent, abbr, lat, lon)


def get_us_states_boundaries():
    """
    Reads the US States Boundaries file.
    :return:
    """
    file_path = get_data_file(US_STATES_BOUNDS_FILE)
    data = None
    with open(file_path) as file:
        data = json.load(file)
    return data


class LocationMapGenerator:
    """
    Creates a LocationMap object. This takes into consideration the type (used as the underlying map)
    and the location. If the location is more detailed than a state, a star is generated on the map
    where the location exists.

    If this generator is called and a map already exists, that is returned.

    """

    def __init__(self, domain):
        self.domain = domain

    def get_or_generate_location_map(self, type, location):
        map = LocationMap.objects.filter(location=location, type=type).first()
        if not map:
            url, base_map = self.__get_base_map(type, location)
            coord_obj = None
            location_bounds_location_obj = None
            if location.geocoordinate:
                coord_obj = location.geocoordinate
            elif location.zipcode:
                coord_obj = location.zipcode.geocoordinate
            elif location.city:
                coord_obj = location.city.geocoordinate
            elif location.county:
                coord_obj = location.county.geocoordinate
            if location.state:
                location_bounds_location_obj = Location.objects.get(state=location.state, city=None)
            location_bounds = None
            if location_bounds_location_obj:
                location_bounds = LocationBounds.objects.get(location=location_bounds_location_obj)

            # If we have a coordinate, that means we have a specific spot to build a generated detailed map on.
            map = LocationMap()
            map.location = location
            map.type = type
            if coord_obj:
                combined_image = self.__generate_detail_map_image(base_map, type, location, location_bounds, coord_obj)
                new_url = self.__save_map_and_return_url_of_detailed_map(type, location, combined_image)
                map.map_file_url = new_url
            else:  # This is the situation where the original base_map needs an entry, but no work is needed.
                map.map_file_url = url
            map.save()
        return map

    def __generate_detail_map_image(self, base_map, type, location, location_bounds, coord_obj):
        if not location_bounds:
            raise Exception('Must have a LocationBounds for {0}'.format(str(location)))

        # 1. Get Star, translate star to be the standard size relative to picture size.
        coord_star = self.__get_star()

        map_file = io.BytesIO(base_map)
        map_image = Image.open(map_file)
        map_width, map_height = map_image.size

        star_x, star_y = Translations.rectangle_reduction(map_width, map_width, MAP_STAR_PERCENTAGE)
        changed_star_file = io.BytesIO()
        with io.BytesIO(coord_star) as star_file:
            im = Image.open(star_file)
            im.thumbnail((star_x, star_y), Image.ANTIALIAS)
            im.save(changed_star_file, "PNG")

        # 2. Find the (x,y) for the coordinate that will be the center point of the star on the map.
        bb_and_map = BoundingBoxAndMap()
        bb_and_map.width = map_width
        bb_and_map.height = map_height
        bb_and_map.bounding_box = location_bounds.get_bounding_box()
        center_x, center_y = bb_and_map.get_coordinate_space(coord_obj.lat, coord_obj.lon)

        # 3. Instead of using the center we need to offset it to the bottom left corner of the star.
        half_x = star_x // 2
        half_y = star_y // 2
        pos_x = center_x - half_x
        pos_y = center_y - half_y

        # 4. Combine Base Map and Star
        overlay = Image.open(changed_star_file).convert("RGBA")
        image_copy = map_image.copy()
        position = (pos_x, pos_y)
        image_copy.paste(overlay, position, mask=overlay)
        combined_image = io.BytesIO()
        image_copy.save(combined_image, format="PNG")

        return combined_image

    def __save_map_and_return_url_of_detailed_map(self, location_type, location, combined_image):
        # 1. Create Url for media storage.
        url = self.__get_url(location_type, location, is_base_map=False)

        # 2. Save to media Storage
        x = default_storage.save(url, combined_image)
        return url

    def __get_url(self, type, location, is_base_map=True):
        url = 'django_geo_db/maps/{type}/{country}/'.format(
            type=type, country=location.country.name.lower().replace(' ', '-'))
        if location.geocoordinate and not is_base_map:
            url += str(location.geocoordinate)
        elif location.zipcode and not is_base_map:
            url += str(location.zipcode.zipcode)
        elif location.city and not is_base_map:
            state = location.state.name.lower().replace(' ', '-')
            url += state + '-'
            url += location.city.name.lower().replace(' ', '-')
        elif location.county and not is_base_map:
            state = location.state.name.lower().replace(' ', '-')
            url += state + '-'
            url += location.county.name.lower().replace(' ', '-')
        elif location.state:
            url += location.state.name.lower().replace(' ', '-')
        elif location.county:
            url += location.county.name.lower().replace(' ', '-')
        else:
            url += location.country.name.lower().replace(' ', '-')
        url += '.png'
        return url

    def __get_base_map(self, type, location):
        url = 'img/' + self.__get_url(type, location)
        url = static(url)
        if 'http' not in url:
            url = self.domain + url
        response = urllib.request.urlopen(url)
        data = response.read()
        return url, data

    def __get_star(self):
        url = static('img/django_geo_db/star.png')
        if 'http' not in url:
            url = self.domain + url
        response = urllib.request.urlopen(url)
        data = response.read()
        return data
