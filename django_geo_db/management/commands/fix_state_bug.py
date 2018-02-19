from django.core.management.base import BaseCommand
from django_geo_db.models import State


class Command(BaseCommand):
    help = "Fixes a state mixup bug."

    def handle(self, *args, **options):
        raise Exception('Make sure you know what you"re doing')
        data = [
            ['New York', 'Montana', 'Maryland'],
            ['Massachusetts', 'North Carolina', 'Nebraska'],
            ['Michigan', 'North Dakota', 'Nevada'],
            ['Mississippi', 'Oklahoma', 'New Jersey'],
            ['New Hampshire', 'Minnesota', 'Ohio'],
            ['New Mexico', 'Missouri', 'Oregon'],
        ]
        for idx in range(len(data)):
            a,b,c = data[idx]
            a = State.objects.get(name=a)
            b = State.objects.get(name=b)
            c = State.objects.get(name=c)
            data[idx] = [a,b,c]
        for a,b,c in data:
            a_coordinate = a.geocoordinate
            b_coordinate = b.geocoordinate
            c_coordinate = c.geocoordinate
            b.geocoordinate = a_coordinate
            c.geocoordinate = b_coordinate
            a.geocoordinate = c_coordinate
            b.save()
            a.save()
            c.save()
