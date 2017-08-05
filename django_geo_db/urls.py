from django_geo_db import views
from django.conf.urls import url

model_urls = [
    url(r'^api/v1/geocoordinate/(?P<pk>\d+)/$', views.GeoCoordinateDetails.as_view(), name='geocoordinate-detail'),
    url(r'^api/v1/continent/(?P<pk>\d+)/$', views.ContinentDetails.as_view(), name='continent-detail'),
    url(r'^api/v1/country/(?P<pk>\d+)/$', views.CountryDetails.as_view(), name='country-detail'),
    url(r'^api/v1/state/(?P<pk>\d+)/$', views.StateDetails.as_view(), name='state-detail'),
    url(r'^api/v1/city/(?P<pk>\d+)/$', views.CityDetails.as_view(), name='city-detail'),
    url(r'^api/v1/zipcode/(?P<pk>\d+)/$', views.ZipcodeDetails.as_view(), name='zipcode-detail'),
    url(r'^api/v1/location/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view(), name='location-detail'),

    url(r'^api/v1/geocoordinate/', views.GeoCoordinateList.as_view(), name='geocoordinate-list'),
    url(r'^api/v1/continent/', views.ContinentList.as_view(), name='continent-list'),
    url(r'^api/v1/country/', views.CountryList.as_view(), name='country-list'),
    url(r'^api/v1/city/', views.CityList.as_view(), name='city-list'),
    url(r'^api/v1/state/', views.StateList.as_view(), name='state-list'),
    url(r'^api/v1/zipcode/', views.ZipcodeList.as_view(), name='zipcode-list'),
    url(r'^api/v1/location/', views.LocationList.as_view(), name='location-list'),
]

