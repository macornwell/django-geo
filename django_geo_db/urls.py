from django_geo_db import views
from django.conf.urls import url

urlpatterns = [
    url(r'geolocate/', views.GeoLocate.as_view(), name='geolocate'),

    url(r'^geocoordinates/(?P<pk>\d+)/$', views.GeoCoordinateDetails.as_view(), name='geocoordinate-detail'),
    url(r'^continents/(?P<pk>\d+)/$', views.ContinentDetails.as_view(), name='continent-detail'),
    url(r'^countries/(?P<pk>\d+)/$', views.CountryDetails.as_view(), name='country-detail'),
    url(r'^state/(?P<pk>\d+)/$', views.StateDetails.as_view(), name='state-detail'),
    url(r'^counties/(?P<pk>\d+)/$', views.CountyDetails.as_view(), name='county-detail'),
    url(r'^cities/(?P<pk>\d+)/$', views.CityDetails.as_view(), name='city-detail'),
    url(r'^zipcodes/(?P<pk>\d+)/$', views.ZipcodeDetails.as_view(), name='zipcode-detail'),
    url(r'^locations/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view(), name='location-detail'),
    url(r'^state-regions/(?P<pk>[0-9]+)/$', views.StateRegionDetails.as_view(), name='state-region-detail'),

    url(r'^geocoordinates/$', views.GeoCoordinateList.as_view(), name='geocoordinate-list'),
    url(r'^continentsx/$', views.ContinentList.as_view(), name='continent-list'),
    url(r'^countries/$', views.CountryList.as_view(), name='country-list'),
    url(r'^counties/$', views.CountyList.as_view(), name='county-list'),
    url(r'^cities/$', views.CityList.as_view(), name='city-list'),
    url(r'^states/$', views.StateList.as_view(), name='state-list'),
    url(r'^zipcodes/$', views.ZipcodeList.as_view(), name='zipcode-list'),
    url(r'^locations/$', views.LocationList.as_view(), name='location-list'),
    url(r'^state-regions/$', views.StateRegionList.as_view(), name='state-region-list'),


    url(r'^location-map/$', views.LocationMapView.as_view(), name='location-map'),
    url(r'^location-map-type/(?P<pk>[0-9]+)/$', views.LocationMapTypeDetail.as_view(), name='locationmaptype-detail'),
    url(r'^plot/(?P<map_type>[a-zA-Z\-]+)/(?P<location_type>[a-zA-Z0-9\-]+)/(?P<country_name>[a-zA-Z0-9\-]+)/(?P<location_name>[a-zA-Z0-9\-]+)/$', views.PlotMap.as_view(), name='plot-map'),
    url(r'^plot-status/(?P<pk>[0-9]+)/$', views.PlottedMapStatus.as_view(), name='plottedmap-status'),
    url(r'^plotted-map/(?P<pk>[0-9]+)/$', views.PlottedMapDetail.as_view(), name='plottedmap-detail'),
]

