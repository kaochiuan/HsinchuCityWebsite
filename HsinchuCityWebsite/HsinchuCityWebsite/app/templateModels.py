
class temple(object):
    def __init__(self, name, locateRegion, mastergod, religiousBelief, organizationType, location, phone1, phone2):
        self.name = name
        self.locateRegion = locateRegion
        self.mastergod = mastergod
        self.religiousBelief = religiousBelief
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

class cultureActiviy(object):
    def __init__(self, activityTheme, startDate, endDate, time, name, locationName, location):
        self.activityTheme = activityTheme
        self.startDate = startDate
        self.endDate = endDate
        self.time = time
        self.name = name
        self.locationName = locationName
        self.location = location

class cityNewes(object):
    def __init__(self, title, publishDate, endDate, type, content, picturePath):
        self.title = title
        self.publishDate = publishDate
        self.endDate = endDate
        self.type = type
        self.content = content
        self.picturePath = picturePath

class hospitalReputation(object):
    def __init__(self, name, location, positiveReputation, negativeReputation ):
        self.name = name
        self.location = location
        self.positiveReputation = positiveReputation
        self.negativeReputation = negativeReputation