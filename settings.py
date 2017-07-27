
class GoogleMapsSettings:
    lat = None
    lon = None
    zoom = None

    def __init__(self, *args, **kwargs):
        for k in kwargs.keys():
            if k in ['lat', 'lon', 'zoom']:
                self.__setattr__(k, kwargs[k])
