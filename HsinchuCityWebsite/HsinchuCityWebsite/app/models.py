"""
Definition of models.
"""

from django.db import models

# Create your models here.

class god(object):
    def __init__(self, temple, region, mastergod, type, organizationType, location, phone1, phone2):
        self.temple = temple
        self.region = region
        self.mastergod = mastergod
        self.type = type
        self.organizationType = organizationType
        self.location = location
        self.phone1 = phone1
        self.phone2 = phone2

class latlng(object):
    def __init__(self, lat,lng):
        self.lat = lat
        self.lng = lng

class location(object):
    def __init__(self, address, latlng):
        self.address = address
        self.latlng = latlng