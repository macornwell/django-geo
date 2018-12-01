from django import forms
from dal.autocomplete import ModelSelect2
from django_geo_db.models import UserLocation, City, Location, GeoCoordinate, Region, LocationMap, LocationBounds, Zipcode
from django_geo_db.widgets import GeocoordinateWidget


class GeocoordinateForm(forms.ModelForm):
    class Meta:
        model = GeoCoordinate
        fields = [
            'generated_name',
            'lat',
            'lon',
        ]
        widgets = {
            'generated_name': GeocoordinateWidget
        }


class UserLocationForm(forms.ModelForm):
    class Meta:
        model = UserLocation
        widgets = {
            'location': ModelSelect2(url='location-autocomplete')
        }
        fields = '__all__'



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        widgets = {
            'zipcode': ModelSelect2(url='zipcode-autocomplete'),
            'city': ModelSelect2(url='city-autocomplete'),
            'county': ModelSelect2(url='county-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            }
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        widgets = {
            'country': ModelSelect2(url='country-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            }
        fields = '__all__'


class LocationMapForm(forms.ModelForm):
    class Meta:
        model = LocationMap
        widgets = {
            'location': ModelSelect2(url='location-autocomplete'),
            }
        fields = '__all__'



class LocationBoundsForm(forms.ModelForm):
    class Meta:
        model = LocationBounds
        widgets = {
            'location': ModelSelect2(url='location-autocomplete'),
            }
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        widgets = {
            'zipcode': ModelSelect2(url='zipcode-autocomplete'),
            'county': ModelSelect2(url='county-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            }
        fields = '__all__'


class ZipcodeChoiceField(forms.ModelChoiceField):

    def __init__(self, **kwargs):
        super(ZipcodeChoiceField, self).__init__(
            queryset=Zipcode.objects.all(),
            widget=ModelSelect2(url='simple-zipcode-autocomplete'),
            **kwargs
        )

    def label_from_instance(self, zipcode):
        return zipcode.zipcode
