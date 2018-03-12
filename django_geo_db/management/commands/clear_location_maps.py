from django.core.management.base import BaseCommand
from django_geo_db.models import LocationMap
from django.core.files.storage import default_storage
from django.db import transaction

@transaction.atomic
class Command(BaseCommand):
    help = "Deletes all Location Maps and clears them from the file system."

    def handle(self, *args, **options):
        for m in LocationMap.objects.all():
            url = m.map_file_url
            if 'static' in url:
                continue
            else:
                print('Deleting Map: {0}'.format(url))
                default_storage.delete(url)
            print('Deleting Obj: {0}'.format(m))
            m.delete()

