import os
import csv
import json
import urllib.request

from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.files.storage import default_storage

from django_geo_db import models
from django_geo_db.utilities import MarkedMap
from django_geo_db.storage import DataStorage


US_CITIES_FILE = 'us-data-final.csv'
US_STATES_FILE = 'us-states.csv'
COUNTRIES_FILE = 'countries.csv'
US_STATES_BOUNDS_FILE = 'us-state-boundaries.json'

US_TERRITORIES = [
    'American Samoa',
    'Federated States Of Micronesia',
    'Guam',
    'Marshall Islands',
    'Northern Mariana Islands',
    'Palau',
    'Puero Rico',
    'Puerto Rico',
    'Saint Thomas',
]


class GeographyDAL:

    def __googlemaps_available(self):
        try:
            import googlemaps
            from django.conf import settings
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            return True
        except:
            return False

    def get_state_by_name(self, state_name):
        return models.State.objects.get(name__iexact=state_name)

    def get_map_type(self, map_type):
        return models.LocationMapType.objects.get(type=map_type)

    def get_location(self, country_name, state_name=None, county_name=None, city_name=None, zipcode=None, name=None, street_address=None):
        result = models.Location.objects.filter(country__name__iexact=country_name)
        if zipcode:
            result = result.filter(zipcode__zipcode=zipcode).first()
            return result
        if state_name:
            result = result.filter(state__name__iexact=state_name)
        if county_name:
            result = result.filter(county__name__iexact=county_name)
        if city_name:
            result = result.filter(city__name__iexact=city_name)
        if name:
            result = result.filter(name__iexact=name)
        if street_address:
            result = result.filter(street_address__iexact=street_address)
        return result.first()

    def get_location_specific(self, country_name, state_name=None, county_name=None,
                              city_name=None, zipcode=None, name=None, street_address=None):
        result = models.Location.objects.filter(country__name__iexact=country_name)
        result = result.filter(zipcode__zipcode=zipcode)
        result = result.filter(state__name__iexact=state_name)
        result = result.filter(county__name__iexact=county_name)
        result = result.filter(city__name__iexact=city_name)
        result = result.filter(name__iexact=name)
        result = result.filter(street_address__iexact=street_address)
        return result.first()

    def get_region(self, country_name, region):
        result = models.Location.objects.filter(country__name__iexact=country_name, region__name__iexact=region).first()
        return result

    def get_boundary_for_us_state(self, state):
        models.LocationBounds

    def get_us_country(self):
        return models.Country.objects.get(name='United States of America')

    def get_us_country_location(self):
        return self.get_location_specific(country_name='United States of America')

    def get_us_states(self):
        return models.State.objects.filter(country=self.get_us_country()).exclude(name__in=US_TERRITORIES).order_by('name')

    def get_city_by_id(self, city_id):
        return models.City.objects.get(pk=city_id)

    def get_country_by_name(self, name):
        country = models.Country.objects.filter(name__iexact=name).first()
        return country

    def get_all_named_locations(self, include_private=False):
        objects = models.Location.objects.filter(name__isnull=False)
        return objects

    def get_location_by_id(self, id):
        return models.Location.objects.get(pk=id)

    def get_users_locations(self, user):
        return models.Usermodels.Location.objects.filter(user=user).values_list('location', flat=True)

    def append_user_location(self, user, locationUsedByUser):
        obj, created = models.Usermodels.Location.objects.get_or_create(user=user, location=locationUsedByUser)
        if not created:
            obj.save()  # This triggers the updating of the date.

    def get_zipcode_by_zip(self, zipcode):
        return models.Zipcode.objects.get(zipcode=zipcode)

    def does_zipcode_exist(self, zipcode):
        return models.Zipcode.objects.filter(zipcode=zipcode).exists()

    def get_zipcode_by_id(self, zipcode_id):
        return models.Zipcode.objects.get(zipcode_id=zipcode_id)

    def create_zipcode(self, city, zipcode, timezone, geocoordinate=None):
        if not geocoordinate:
            geocoordinate = city.geocoordinate
        return models.Zipcode.objects.create(city=city, zipcode=zipcode, geocoordinate=geocoordinate, timezone=timezone)

    def create_location(self, zipcode, coordinate, name):
        city = zipcode.city
        state = city.state
        country = state.country
        location, created = models.Location.objects.get_or_create(country=country, state=state, city=city, zipcode=zipcode,
                                                           geocoordinate=coordinate, name=name)
        return location

    def get_or_create_street_address_location(self, street_address, zipcode):
        city = zipcode.city
        state = city.state
        country = state.country
        location, created = models.Location.objects.get_or_create(country=country, state=state, city=city, zipcode=zipcode,
                                                           street_address=street_address)
        if created and not location.geocoordinate:
            if self.__googlemaps_available():
                try:
                    lat, lon = self.geocode_location_get_lat_lon(location)
                    geocoordinate = self.get_or_create_geocoordinate(lat, lon)
                    location.geocoordinate = geocoordinate
                    location.save()  # This will set the name as well.
                except Exception as e:
                    print(e)
                    pass
        return location, created

    def geocode_location_get_lat_lon(self, location):
        import googlemaps
        from django.conf import settings
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        geocode_result = gmaps.geocode(str(location))
        result = geocode_result[0]
        geo_coord = result['geometry']['location']
        lat = geo_coord['lat']
        lon = geo_coord['lng']
        return lat, lon

    def get_or_create_geocoordinate(self, lat, lon):
        lat_neg, lat_tens, lat_ones, lat_tenths, lat_hundredths, lat_thousands, lat_ten_thousands, other2 = models.GeoCoordinate.split_lat_coordinate(str(lat))
        lon_neg, lon_hundreds, lon_tens, lon_ones, lon_tenths, lon_hundredths, lon_thousands, lon_ten_thousands, other2 = models.GeoCoordinate.split_lon_coordinate(str(lon))
        coord = models.GeoCoordinate.objects.filter(lat_neg=lat_neg, lat_tens=lat_tens, lat_ones=lat_ones,
                                             lat_tenths=lat_tenths, lat_hundredths=lat_hundredths,
                                             lat_thousands=lat_thousands, lat_ten_thousands=lat_ten_thousands,
                                             lon_neg=lon_neg, lon_hundreds=lon_hundreds, lon_tens=lon_tens,
                                             lon_ones=lon_ones, lon_tenths=lon_tenths, lon_hundredths=lon_hundredths,
                                             lon_ten_thousands=lon_ten_thousands).first()
        if not coord:
            coord = models.GeoCoordinate()
            coord.lat = lat
            coord.lon = lon
            coord.save()
        return coord

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
                zipcodeObj = models.Zipcode.objects.get(zipcode=zipcode)
                break
        return zipcodeObj


    def geolocate(self, strings_list):
        """
        GeoLocate's a list of strings. This works internally without using Google's services.
        Query Format:
        United States of America (Country)
        Virginia (State)
        Montgomery County, Virginia (County)
        Blacksburg, Virginia (State)
        :param strings_list:
        :return:
        """
        results = []
        county_words = [
            ' county',
            ' parish',
            ' borough',
        ]
        for q in strings_list:
            location = None
            # Is this a city or county query?
            if ',' in q:
                value, state = q.split(',')
                value = value.strip()
                state = state.strip()
                is_county = False
                lowered_value = value.lower()
                for c in county_words:
                    index = lowered_value.find(c)
                    if index > -1:
                        value = value[0:index]
                        is_county = True
                        break
                value = value.strip()
                if is_county:
                    location = models.Location.objects.filter(county__name__iexact=value, state__name__iexact=state,
                                                       city=None).first()
                else:
                    location = models.Location.objects.filter(city__name__iexact=value, state__name__iexact=state,
                                                       zipcode__isnull=True).first()
            else:
                location = models.Location.objects.filter(Q(country__name__iexact=q, state=None, region=None) |
                                                   Q(state__name__iexact=q, city=None, county=None)).first()
            results.append(location)
        return results

    def does_geographic_shape_exist(self, name):
        return models.GeographicShape.objects.filter(name=name).exists()

    def create_geographic_shape(self, name):
        shape = models.GeographicShape.objects.create(name=name)
        return shape

    def create_geographic_shape_coordinate(self, geographic_shape_id, order, lat, lon):
        geocoordinate = self.get_or_create_geocoordinate(lat, lon)
        return models.GeographicShapeCoordinate.objects.create(geographic_shape_id=geographic_shape_id, geocoordinate=geocoordinate, order=order)

    def delete_geographic_shape(self, geographic_shape_id):
        models.GeographicShape.objects.get(pk=geographic_shape_id).delete()

    def delete_geographic_shape_coordinate(self, geographic_shape_coordinate_id):
        models.GeographicShapeCoordinate.objects.get(pk=geographic_shape_coordinate_id).delete()


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


class GeographicShapeBuilder:

    def list_us_shape_data(self):
        data = get_us_states_boundaries()
        states = data['states']['state']
        for state in states:
            name = state['-name']
            points = state['point']
            yield (name, points)

    def create_us_states_geographic_shapes(self):
        for name, points in self.list_us_shape_data():
            shape, shape_coordinates = self.create_geographic_shapes(name, points)

    def create_geographic_shapes(self, name, boundary_dict_list):
        shape = GEO_DAL.create_geographic_shape(name)
        points = []
        try:
            order = 1
            for p in boundary_dict_list:
                lat = float(p["-lat"])
                lon = float(p["-lng"])
                point = GEO_DAL.create_geographic_shape_coordinate(shape.pk, order, lat, lon)
                points.append(point)
                order += 1
        except Exception as e:
            for p in points:
                GEO_DAL.delete_geographic_shape_coordinate(p.pk)
            GEO_DAL.delete_geographic_shape(shape.pk)
            raise e
        return (shape, points)


class LocationMapGenerator:
    """
    Creates a models.LocationMap object. This takes into consideration the type (used as the underlying map)
    and the location. If the location is more detailed than a state, a star is generated on the map
    where the location exists.

    If this generator is called and a map already exists, that is returned.

    """

    def __init__(self, domain):
        self.domain = domain

    def get_regional_map(self, type, location):
        map = models.LocationMap.objects.filter(location=location, type=type).first()
        if not map:
            url = 'img/django_geo_db/maps/{0}/{1}/{2}.png'.format(type, location.country.name.replace(' ', '-').lower(),
                                                                  location.region.name.replace(' ', '-').lower())
            url, base_map = self.__get_map(url)
            map = models.LocationMap()
            map.location = location
            map.type = type
            map.map_file_url = url
            map.save()
        return map

    def get_or_generate_location_map(self, type, location):
        map = models.LocationMap.objects.filter(location=location, type=type).first()
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
                location_bounds_location_obj = models.Location.objects.get(state=location.state, county=None, city=None)
            if coord_obj and not location_bounds_location_obj:
                location_bounds_location_obj = location
            location_bounds = None
            if location_bounds_location_obj:
                location_bounds = models.LocationBounds.objects.get(location=location_bounds_location_obj)

            # If we have a coordinate, that means we have a specific spot to build a generated detailed map on.
            map = models.LocationMap()
            map.location = location
            map.type = type
            if coord_obj:
                combined_image = self.__add_star_to_base_map(base_map, location_bounds, coord_obj)
                new_url = self.__save_map_and_return_url_of_detailed_map(type, location, combined_image)
                map.map_file_url = new_url
            else:  # This is the situation where the original base_map needs an entry, but no work is needed.
                map.map_file_url = url
            map.save()
        return map

    def __add_star_to_base_map(self, base_map_bytes, location_bounds, coord_obj):
        storage = DataStorage(self.domain)
        map = MarkedMap(storage, base_map_bytes, location_bounds)
        combined_image = map.add_star_to_base_map(coord_obj, marker_size=0.05)
        return combined_image

    def __save_map_and_return_url_of_detailed_map(self, location_type, location, combined_image):
        # 1. Create Url for media storage.
        url = self.__get_url(location_type, location, is_base_map=False)

        # 2. Save to media Storage
        x = default_storage.save(url, combined_image)
        return url

    def __get_url_for_named_location(self, type, name):
        url = 'django_geo_db/maps/{type}/{name}.png'.format(type=type, name=name)
        return url

    def __get_url(self, type, location, is_base_map=True):
        url = 'django_geo_db/maps/{type}/{country}/'.format(
            type=type, country=location.country.name.lower().replace(' ', '-'))
        if location.geocoordinate and not is_base_map:
            url += str(location.geocoordinate)
        elif location.zipcode and not is_base_map:
            state = location.state.name.lower().replace(' ', '-')
            url += state + '-'
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
        elif location.name:
            url += location.name.lower().replace(' ', '-')
        else:
            url += location.country.name.lower().replace(' ', '-')
        url += '.png'
        return url

    def __get_map(self, url):
        url = static(url)
        if 'http' not in url:
            url = self.domain + url
        response = urllib.request.urlopen(url)
        data = response.read()
        return url, data

    def __get_map_for_named_location(self, type, name):
        url = 'img/' + self.__get_url_for_named_location(type, name)
        return self.__get_map(url)

    def __get_base_map(self, type, location):
        url = 'img/' + self.__get_url(type, location)
        return self.__get_map(url)
