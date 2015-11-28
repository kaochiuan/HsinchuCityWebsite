"""
Definition of models.
"""

from django.db import models
from django.db.models.query_utils import Q

# TempleInfo & Manager.
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

# CultureActivity & Manager
class CultureActiviyManager(models.Manager):
    def create_activity(self,name,activityTheme,locationName,address,latitude,longitude,startDate,endDate,activityTime):
        activity = self.create(name=name, activityTheme=activityTheme, locationName=locationName,
                             address=address, latitude=latitude, longitude=longitude,
                             startDate=startDate, endDate=endDate,activityTime=activityTime)
        return activity
    def filter_activity(self,name,activityTheme,locationName,address,startDate,endDate):
        activity = self.filter(name = name, activityTheme = activityTheme, locationName = locationName, 
                               address = address, startDate = startDate, endDate = endDate);
        return activity
    def filterByKeyword(self,keyword):
        activity = self.filter_activity(Q(name__contains=keyword) | Q(endDate__contains=keyword) | Q(startDate__contains=keyword) | 
                                        Q(activityTheme__contains=keyword) | Q(locationName__contains=keyword) | Q(address__contains=keyword))
        return activity
class CultureActiviyInfo(models.Model):
    activityTheme = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    activityTime = models.CharField(max_length=50)
    locationName = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    startDate = models.CharField(max_length=50)
    endDate = models.CharField(max_length=50)
    objects = CultureActiviyManager()

    def __unicode__(self):
        return str.format("{0}_{1}",self.name,self.startDate)

# CityNews & Manager
class CityNewsManager(models.Manager):
    def create_news(self,title,type,content,publishDate,endDate,picturePath):
        news = self.create(title=title, type=type, content=content,
                             publishDate=publishDate, endDate=endDate, picturePath=picturePath)
        return news
    def filter_news(self,title,type,publishDate,endDate):
        news = self.filter(title = title, type = type, publishDate = publishDate, 
                               endDate = endDate);
        return news
    def filterByDate(self,start,end):
        news = self.filter_activity(Q(publishDate__range=[start, end]) | Q(endDate__range=[start, end]))
        return news
class CityNewsItem(models.Model):
    title = models.CharField(max_length=300)
    type = models.CharField(max_length=50)
    content = models.TextField()
    publishDate = models.DateField()
    endDate = models.DateField()
    picturePath = models.URLField()
    objects = CityNewsManager()
    
    def __unicode__(self):
        return str.format("{0}_{1}",self.title,self.publishDate)

