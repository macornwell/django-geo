from django.contrib import admin

from openfruit.geography.models import Location, City, Continent, Country, \
    State, GeoCoordinate, UserLocation
from openfruit.geography.forms import UserLocationForm, LocationForm, CityForm, GeocoordinateForm


class UserLocationAdmin(admin.ModelAdmin):
    form = UserLocationForm

class LocationAdmin(admin.ModelAdmin):
    form = LocationForm

class CityAdmin(admin.ModelAdmin):
    form = CityForm

class GeocoordinateAdmin(admin.ModelAdmin):
    form = GeocoordinateForm




admin.site.register(City, CityAdmin)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(GeoCoordinate, GeocoordinateAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(Location, LocationAdmin)


