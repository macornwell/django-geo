from django.core.management.base import BaseCommand
from django_geo_db.models import Location, GeographicRegion, State, Country

SOUTHEAST = [
    'Virginia',
    'North Carolina',
    'South Carolina',
    'Tennessee',
    'Georgia',
    'Alabama',
    'Florida',
    'Louisiana',
    'Texas',
    'Mississippi',
]

class Command(BaseCommand):
    help = "Generates the default Geographic Regions."

    def __get_or_create_region(self, country, name, state_list):
        region = GeographicRegion.objects.filter(name=name)
        if len(region) < 1:
            print('Creating ' + name)
            region = GeographicRegion()
            region.name = name
            region.save()
            states = State.objects.filter(country=country, name__in=state_list)
            if len(states) < 1:
                raise Exception('No states found for {0} list.'.format(name))
            locations = Location.objects.filter(state__in=states, city=None, county=None)
            if len(states) < 1:
                raise Exception('No locations found for {0} list.'.format(name))
            region.locations = locations
            region.save()
        else:
            pass

    def handle(self, *args, **options):
        us = Country.objects.get(name__iexact='United States of America')
        print('Generating Southeast')
        self.__get_or_create_region(us, 'Southeast', SOUTHEAST)


