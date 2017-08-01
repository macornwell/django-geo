from django.core.management.base import BaseCommand
from django_geo_db.models import Location, Zipcode, City, State, GeoCoordinate
from django.db import IntegrityError, transaction

@transaction.atomic
class Command(BaseCommand):
    help = "Sets up all of the generated names of geo objects"

    def __generate(self, modelType):
        models = modelType.objects.all()
        count = models.count()
        print('Generating {0}: {1}'.format(modelType.__name__, count))
        buffer = []
        for index in range(count):
            l = models[index]
            buffer.append(l)
            if len(buffer) > 1000:
                try:
                    with transaction.atomic():
                        for l in buffer:
                            l.save()
                    print('Saved {0}'.format(index))
                except IntegrityError as e:
                    print('Exception occurred while committing.')
                    raise e
                buffer = []

    def handle(self, *args, **options):
        self.__generate(Location)
        self.__generate(Zipcode)
        self.__generate(City)
        self.__generate(State)
        self.__generate(GeoCoordinate)


