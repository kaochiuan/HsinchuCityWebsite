"""
Definition of models.
"""

from django.db import models

class god(object):
    def __init__(self, temple, region, mastergod, type, organizationType, address, phone1, phone2):
        self.temple = temple
        self.region = region
        self.mastergod = mastergod
        self.type = type
        self.organizationType = organizationType
        self.address = address
        self.phone1 = phone1
        self.phone2 = phone2


# Create your models here.
