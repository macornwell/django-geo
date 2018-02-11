from django_geo_db import autocomplete_views as views
from django.conf.urls import url

urlpatterns = [
    url('^autocomplete/named-location/$',
        views.NamedLocationAutocomplete.as_view(),
        name='named-location-autocomplete'),
    url('^autocomplete/location/$',
        views.LocationAutocomplete.as_view(),
        name='location-autocomplete'),
    url('^autocomplete/public-locations/$',
        views.PublicLocationsAutocomplete.as_view(),
        name='public-locations-autocomplete'),
    url('^autocomplete/zipcode/$',
        views.ZipcodeAutocomplete.as_view(),
        name='zipcode-autocomplete'),
    url('^autocomplete/county/$',
        views.CountyAutocomplete.as_view(),
        name='county-autocomplete'),
    url('^autocomplete/city/$',
        views.CityAutocomplete.as_view(),
        name='city-autocomplete'),
    url('^autocomplete/geocoordinate/$',
        views.GeoCoordinateAutocomplete.as_view(),
        name='geocoordinate-autocomplete'),
]
