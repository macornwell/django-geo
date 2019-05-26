from django import forms
from dal.autocomplete import ModelSelect2
from django_geo_db import models
from django_geo_db.widgets import GeocoordinateWidget
from django_geo_db.services import GEO_DAL


class AddUSZipcodeForm(forms.Form):
    zipcode = forms.IntegerField(min_value=1, max_value=99999)
    timezone = forms.ChoiceField(choices=models.US_TIMEZONE_CHOICES)
    city = forms.ModelChoiceField(
        queryset=models.City.objects.all(),
        widget=ModelSelect2(url='city-autocomplete'),
    )

    def clean(self):
        cleaned_data = super(AddUSZipcodeForm, self).clean()
        zipcode = int(self.data.get('zipcode'))
        city = self.data.get('city')

        if GEO_DAL.does_zipcode_exist(zipcode):
            self.add_error('zipcode', "This zipcode already exists.")
        if not city:
            self.add_error('city', 'Must have city')
        return


class GeocoordinateForm(forms.ModelForm):
    class Meta:
        model = models.GeoCoordinate
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
        model = models.UserLocation
        widgets = {
            'location': ModelSelect2(url='location-autocomplete')
        }
        fields = '__all__'



class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        widgets = {
            'zipcode': ModelSelect2(url='zipcode-autocomplete'),
            'city': ModelSelect2(url='city-autocomplete'),
            'county': ModelSelect2(url='county-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            }
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model = models.Region
        widgets = {
            'country': ModelSelect2(url='country-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            }
        fields = '__all__'


class LocationMapForm(forms.ModelForm):
    class Meta:
        model = models.LocationMap
        widgets = {
            'location': ModelSelect2(url='location-autocomplete'),
            }
        fields = '__all__'



class LocationBoundsForm(forms.ModelForm):
    class Meta:
        model = models.LocationBounds
        widgets = {
            'location': ModelSelect2(url='location-autocomplete'),
            }
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        model = models.City
        widgets = {
            'zipcode': ModelSelect2(url='zipcode-autocomplete'),
            'county': ModelSelect2(url='county-autocomplete'),
            'geocoordinate': ModelSelect2(url='geocoordinate-autocomplete'),
            }
        fields = '__all__'


class ZipcodeChoiceField(forms.ModelChoiceField):

    def __init__(self, **kwargs):
        super(ZipcodeChoiceField, self).__init__(
            queryset=models.Zipcode.objects.all(),
            widget=ModelSelect2(url='simple-zipcode-autocomplete'),
            **kwargs
        )

    def label_from_instance(self, zipcode):
        return zipcode.zipcode
