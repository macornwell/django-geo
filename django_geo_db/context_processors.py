from django.conf import settings
from django_geo_db.services import GEO_DAL


def google_maps_api_key(request):
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}


def google_maps_settings(request):
    return {'GM_SETTINGS': settings.GM_SETTINGS}

