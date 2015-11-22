
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