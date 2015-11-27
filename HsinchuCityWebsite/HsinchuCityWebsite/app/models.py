"""
Definition of models.
"""

from django.db import models

# Create your models here.
class TempleManager(models.Manager):
    def create_temple(self,name,locateRegion,religiousBelief,masterGod,address,latitude,longitude,phone1,phone2):
        temple = self.create(name=name, locateRegion=locateRegion, religiousBelief=religiousBelief,
                             masterGod=masterGod, address=address, latitude=latitude, longitude=longitude,
                             phone1=phone1, phone2=phone2)
        return temple

    def filter_temple(self,name,locateRegion,masterGod):
        temple = self.filter(name=name, locateRegion=locateRegion,  masterGod=masterGod)
        return temple

    def filterByMasterGod(self, masterGod):
        temple = self.filter(masterGod = masterGod)
        return temple

    def filterByRegion(self, locateRegion):
        temple = self.filter(locateRegion = locateRegion)
        return temple

    def filterByReligiousBelief(self, religiousBelief):
        temple = self.filter(religiousBelief = religiousBelief)
        return temple

    def getAll(self):
        return self.all()

    def filterByDetail(self, locateRegion, religiousBelief):
        location = locateRegion.strip()
        belief = religiousBelief.strip()
        if location.isspace():
            if belief.isspace():
                temple = self.all()
            else:
                temple = self.filter(religiousBelief = religiousBelief)
        elif belief.isspace():
            temple = self.filter(locateRegion = locateRegion)
        else:
            temple = self.filter(locateRegion = locateRegion, religiousBelief = religiousBelief)
        return temple

    def getDistinctRegion(self):
        temple = self.order_by('locateRegion').distinct('locateRegion')
        return temple

    def getDistinctReligiousBelief(self):
        temple = self.order_by('religiousBelief').distinct('religiousBelief')
        return temple

    def getDistinctMasterGod(self):
       temple = self.order_by('masterGod').distinct('masterGod')
       return temple


class TempleInfo(models.Model):
    name = models.CharField(max_length=50)
    locateRegion = models.CharField(max_length=10)
    religiousBelief = models.CharField(max_length=50)
    masterGod = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone1 = models.CharField(max_length=20,blank=True)
    phone2 = models.CharField(max_length=20,blank=True)
    objects = TempleManager()

    def __unicode__(self):
        return self.name

