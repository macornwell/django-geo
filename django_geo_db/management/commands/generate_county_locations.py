from django.core.management.base import BaseCommand
from django_geo_db.models import Location, County

class Command(BaseCommand):
    help = "Creates County Locations if they do not currently exist."

    def handle(self, *args, **options):
        for county in County.objects.all():
            location, created = Location.objects.get_or_create(country=county.state.country, state=county.state,
                                                               county=county, city=None, zipcode=None)
            if created:
                print('Created {0}'.format(location))
