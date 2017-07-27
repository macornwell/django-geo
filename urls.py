from django_geo import views
from django_geo.views import LocationAutocomplete, ZipcodeAutocomplete, CityAutocomplete, GeoCoordinateAutocomplete, NamedLocationAutocomplete, PublicLocationsAutocomplete, LocationList
from django.conf.urls import url


urlpatterns = [
    url('^autocomplete/named-location/$',
        NamedLocationAutocomplete.as_view(),
        name='named-location-autocomplete'),
    url('^autocomplete/location/$',
        LocationAutocomplete.as_view(),
        name='location-autocomplete'),
    url('^autocomplete/public-locations/$',
        PublicLocationsAutocomplete.as_view(),
        name='public-locations-autocomplete'),
    url('^autocomplete/zipcode/$',
        ZipcodeAutocomplete.as_view(),
        name='zipcode-autocomplete'),
    url('^autocomplete/city/$',
        CityAutocomplete.as_view(),
        name='city-autocomplete'),
    url('^autocomplete/geocoordinate/$',
        GeoCoordinateAutocomplete.as_view(),
        name='geocoordinate-autocomplete'),

    url(r'^api/v1/location/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view(), name='location-detail'),
    url(r'^api/v1/location/', LocationList.as_view(), name='location-list'),
]
