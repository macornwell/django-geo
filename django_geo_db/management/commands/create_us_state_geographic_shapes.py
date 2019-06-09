from django.core.management.base import BaseCommand
from django_geo_db.services import GeographicShapeBuilder, GEO_DAL
from django.db import IntegrityError, transaction

@transaction.atomic
class Command(BaseCommand):
    help = "Creates GeographicShapes for each US State. This is useful for showing the boundaries of the states."


    def handle(self, *args, **options):
        builder = GeographicShapeBuilder()
        for name, points in builder.list_us_shape_data():
            if not GEO_DAL.does_geographic_shape_exist(name):
                print('Creating {0}'.format(name))
                builder.create_geographic_shapes(name, points)
            else:
                print('Skipping {0}'.format(name))
