from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib import admin


class Location(models.Model):
    name = models.CharField(max_length=255, default="Unknown name")
    city = models.CharField(max_length=255, default="Unknown city")
    region = models.CharField(max_length=255, default="Unknown region")
    cuisine = models.CharField(max_length=255, default="Unknown cuisine")
    url = models.URLField(default="")
    star_level = models.IntegerField(default=1)
    year = models.IntegerField(default=2000)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    geom = models.PointField(default='POINT(0 0)', srid=4326)
    
    def __str__(self):
        return self.name

admin.site.register(Location)