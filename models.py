from django.db import models
from core.models import BaseUserActivityOnSiteModel, BaseModel


class Continent(BaseModel):
    continent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)


class Country(BaseModel):
    country_id = models.AutoField(primary_key=True)
    continent = models.ForeignKey(Continent)
    name = models.CharField(max_length=50, unique=True)


class State(BaseModel):
    state_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = (('country', 'name'),)


class City(BaseModel):
    city_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(State)
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)

    class Meta:
        unique_together = (('state', 'name'),)


class Location(BaseModel):
    location = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country)
    state = models.ForeignKey(State)
    city = models.ForeignKey(City, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.state.country != self.country:
            raise Exception("The state's country does not match the selected country.")
        if self.city and self.city.state != self.state:
            raise Exception("City's state does not match the selected state.")
        super(BaseModel, self).save(*args, **kwargs)


