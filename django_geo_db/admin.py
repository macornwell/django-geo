from django.contrib import admin

from django_geo_db.models import Location, City, Continent, Country, \
    State, GeoCoordinate, UserLocation, County, Region, LocationMap, LocationBounds
from django_geo_db.forms import UserLocationForm, LocationForm, CityForm, GeocoordinateForm, RegionForm, LocationMapForm


class UserLocationAdmin(admin.ModelAdmin):
    form = UserLocationForm


class RegionAdmin(admin.ModelAdmin):
    form = RegionForm


class LocationAdmin(admin.ModelAdmin):
    form = LocationForm


class CityAdmin(admin.ModelAdmin):
    form = CityForm


class GeocoordinateAdmin(admin.ModelAdmin):
    form = GeocoordinateForm


class LocationMapAdmin(admin.ModelAdmin):
    form = LocationMapForm


admin.site.register(City, CityAdmin)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(County)
admin.site.register(GeoCoordinate, GeocoordinateAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(LocationBounds)
admin.site.register(LocationMap, LocationMapAdmin)


