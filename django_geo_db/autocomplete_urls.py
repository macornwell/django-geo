from django_geo_db import autocomplete_views
from django.conf.urls import url

autocomplete_urls = [
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
    url('^autocomplete/city/$',
        views.CityAutocomplete.as_view(),
        name='city-autocomplete'),
    url('^autocomplete/geocoordinate/$',
        views.GeoCoordinateAutocomplete.as_view(),
        name='geocoordinate-autocomplete'),
]
