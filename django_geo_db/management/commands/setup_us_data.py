from datetime import datetime
from django.core.management.base import BaseCommand
from django_geo_db.models import City, Continent, Country, \
    GeoCoordinate, State, Location, Zipcode
from django_geo_db.services import generate_current_us_cities_list, generate_current_us_states_list, generate_countries
from django_geo_db.utilities import get_standardized_coordinate


def get_minutes(timeDelta):
    seconds = timeDelta.total_seconds()
    minutes = (seconds % 3600) // 60
    return minutes


class Command(BaseCommand):
    help = "Setups all Geographical information for US based cities."


    def __get_geocoordinate(self, lat, lon):
        lat = get_standardized_coordinate(lat)
        lon = get_standardized_coordinate(lon)
        try:
            geoCoord = GeoCoordinate.objects.create(lat=lat, lon=lon)
        except:
            try:
                geoCoord = GeoCoordinate.objects.get(lat=lat, lon=lon)
            except Exception as e:
                print('Lat: {0}, Lon: {1}'.format(lat, lon))
                raise e
        return geoCoord



    def handle(self, *args, **options):
        totalStart = datetime.now()

        print('Populating Continents and Countries')
        start = datetime.now()
        self.create_all_countries_and_continents()
        end = datetime.now()
        print('Continents and Countries took {0} seconds.'.format((end - start).total_seconds()))

        print('Populating US States')
        start = datetime.now()
        self.create_all_us_states()
        end = datetime.now()
        print('US States took {0} seconds.'.format((end - start).total_seconds()))

        print('Populating US Cities and Zips')
        start = datetime.now()
        self.create_all_cities_and_zipcodes()
        end = datetime.now()
        print('US Cities and Zips took {0} minutes.'.format(get_minutes(end - start)))

        totalEnd = datetime.now()
        print('Total import took {0} minutes.'.format(get_minutes(totalEnd - totalStart)))


    def create_all_countries_and_continents(self):
        continents = {}
        count = 0
        for country, continent, abbrev, lat, lon in generate_countries():
            try:
                if continent not in continents:
                    continentObj = Continent.objects.create(name=continent)
                    continents[continent] = continentObj
                geocoordinate = self.__get_geocoordinate(lat, lon)
                countryObj = Country.objects.create(continent=continents[continent], name=country, geocoordinate=geocoordinate, abbreviation=abbrev)
                Location.objects.create(country=countryObj)
                count += 1
            except:
                raise Exception('Exception occurred processing {0} country.'.format(country))



    def create_all_us_states(self):
        locationList = []
        usCountry = Country.objects.get(name='United States of America')
        for state, abbreviation, latitude, longitude in generate_current_us_states_list():
            try:
                geoCoordinate = self.__get_geocoordinate(latitude, longitude)
                stateObj = State(country=usCountry, name=state, abbreviation=abbreviation, geocoordinate=geoCoordinate)
                stateObj.save()
                locationObj = Location(country=usCountry, state=stateObj)
                locationList.append(locationObj)
            except:
                raise Exception('Exception occurred processing {0} state.'.format(state))
        Location.objects.bulk_create(locationList)


    def create_all_cities_and_zipcodes(self):
        count = State.objects.all().count()
        stateDict = {}
        usCountry = Country.objects.get(name='United States of America')
        for state in State.objects.filter(country=usCountry):
            stateDict[state.abbreviation] = state
        uniqueCities = set()
        noLat = []
        for zip, lat, lon, city, state, timezone in generate_current_us_cities_list():
            if not lat:
                noLat.append((zip, lat, lon, city, state, timezone))
                continue
            stateObj = stateDict[state]
            cityObj = None
            try:
                geoCoordinate = self.__get_geocoordinate(lat, lon)
                keyFound = False
                key = '{0}-{1}'.format(state, city)
                if key not in uniqueCities:
                    uniqueCities.add(key)
                    cityObj = City.objects.create(state=stateObj, name=city, geocoordinate=geoCoordinate)
                    Location.objects.create(country=usCountry, state=stateObj, city=cityObj)
                    keyFound = False
                if not cityObj:
                    cityObj = City.objects.get(state=stateObj, name=city)
                    keyFound = True
                zipObj = Zipcode.objects.create(city=cityObj, zipcode=zip, geocoordinate=geoCoordinate, timezone=timezone)
                if stateObj != cityObj.state:
                    raise Exception('{0} is not {1} in city {2}. KeyFound {3}. Key {4}'.format(stateObj, cityObj.state, cityObj, keyFound, key))
                Location.objects.create(country=usCountry, state=stateObj, city=cityObj, zipcode=zipObj)
            except:
                print('zip: ' + zip)
                print('StateObj: ' + str(stateObj))
                print('State: ' + str(state))
                print('Key: ' + str(key))
                raise Exception('Exception occurred while processing Zipcode {0}'.format(zip))
        for zip, lat, lon, city, state, timezone in noLat:
            key = '{0}-{1}'.format(state, city)
            stateObj = stateDict[state]
            cityObj = City.objects.filter(state=stateObj, name=city).first()
            if not cityObj:
                cityObj = City.objects.filter(state=stateObj).first()
            zipObj = Zipcode.objects.create(city=cityObj, zipcode=zip, geocoordinate=cityObj.geocoordinate, timezone=timezone)
            Location.objects.create(country=usCountry, state=stateObj, city=cityObj, zipcode=zipObj)




