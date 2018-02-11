from django_geo_db import views
from django.conf.urls import url

urlpatterns = [
    url(r'^geocoordinate/(?P<pk>\d+)/$', views.GeoCoordinateDetails.as_view(), name='geocoordinate-detail'),
    url(r'^continent/(?P<pk>\d+)/$', views.ContinentDetails.as_view(), name='continent-detail'),
    url(r'^country/(?P<pk>\d+)/$', views.CountryDetails.as_view(), name='country-detail'),
    url(r'^state/(?P<pk>\d+)/$', views.StateDetails.as_view(), name='state-detail'),
    url(r'^county/(?P<pk>\d+)/$', views.CountyDetails.as_view(), name='county-detail'),
    url(r'^city/(?P<pk>\d+)/$', views.CityDetails.as_view(), name='city-detail'),
    url(r'^zipcode/(?P<pk>\d+)/$', views.ZipcodeDetails.as_view(), name='zipcode-detail'),
    url(r'^location/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view(), name='location-detail'),

    url(r'^geocoordinate/', views.GeoCoordinateList.as_view(), name='geocoordinate-list'),
    url(r'^continent/', views.ContinentList.as_view(), name='continent-list'),
    url(r'^country/', views.CountryList.as_view(), name='country-list'),
    url(r'^county/', views.CountyList.as_view(), name='county-list'),
    url(r'^city/', views.CityList.as_view(), name='city-list'),
    url(r'^state/', views.StateList.as_view(), name='state-list'),
    url(r'^zipcode/', views.ZipcodeList.as_view(), name='zipcode-list'),
    url(r'^location/', views.LocationList.as_view(), name='location-list'),
]

