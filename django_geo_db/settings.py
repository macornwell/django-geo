from django.conf import settings

def require_authentication(self):
    require = True 
    try:
        require = settings.GEO_AUTOCOMPLETE_REQUIRES_AUTHENTICATION
    except:
        pass
    return require


class GoogleMapsSettings:
    lat = None
    lon = None
    zoom = None

    def __init__(self, *args, **kwargs):
        for k in kwargs.keys():
            if k in ['lat', 'lon', 'zoom']:
                self.__setattr__(k, kwargs[k])
