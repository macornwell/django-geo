from django.core.management.base import BaseCommand
from django_geo_db.models import GeoCoordinate
from django.db.transaction import atomic


class Command(BaseCommand):
        help = "Calls save on every GeoCoordinate, which will regenerated all auto-generated values."


    @atomic
    def handle(self, *args, **options):
        for coord in GeoCoordinate.objects.all():
            coord.save()
