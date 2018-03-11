from django.core.management.base import BaseCommand
from django_geo_db.models import LocationMapType

TYPES = [
    'simple',
]

class Command(BaseCommand):
    help = "Adds default map types."

    def handle(self, *args, **options):
        for t in TYPES:
            map_type, created = LocationMapType.objects.get_or_create(type=t)
            if created:
                print('Created: {0}'.format(str(map_type)))
