"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse
import urllib.request
import json
import urllib
from urllib.request import Request
from app.models import TempleInfo, TempleManager
from app.templateModels import *
from django.contrib.sites import requests
from django.views.decorators.csrf import csrf_protect
from django.core import serializers

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }))

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }))

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }))

def templeMaps(request):
    assert isinstance(request, HttpRequest)
    regions = TempleInfo.objects.getDistinctRegion()
    belief = TempleInfo.objects.getDistinctReligiousBelief()

    regionLst = []
    beliefLst = []
    for r in regions:
        regionLst.append(r.locateRegion)
    for b in belief:
        beliefLst.append(b.religiousBelief)

    return render(request,
        'app/templeMaps.html',
        context_instance = RequestContext(request,
        {
            'title':'求人不如求神',
            'regions':regionLst,
            'belief':beliefLst,
        }))

@csrf_protect
def filterTemple(request):
    assert isinstance(request, HttpRequest)
    region = request.POST['region']
    belief = request.POST['belief']

    filterTemples = TempleInfo.objects.filterByDetail(region,belief)
    data = serializers.serialize("json", filterTemples)
    return HttpResponse(json.dumps({"status": "Success", "templeInfo": data}),
                        content_type="application/json")


def allMyGodsInHsinchu(request):
    assert isinstance(request, HttpRequest)
    req = Request("http://opendata.hccg.gov.tw/dataset/480911dd-6eea-4f97-a7e8-334b32cc8f6b/resource/ee12c072-e8aa-4be1-8179-f1c9606198f3/download/20150304091340575.json")
    try:
        response = urllib.request.urlopen(req)
        ur = response.readall().decode('utf-8-sig')
        j_obj = json.loads(ur) 
        templeLst = []

        for jsonObj in j_obj:
            address = jsonObj["寺廟所在地"]
            success, lat, lng = AddressToLatlng(address)
            if success == True:
                wgs84locate = latlng(lat, lng)
                loc = location(address,wgs84locate)
            else:
                wgs84locate = latlng(0.0, 0.0)
                loc = location(address,wgs84locate)

            g = temple(jsonObj["寺廟名稱"],jsonObj["地區"],jsonObj["主祀神像"],jsonObj["教別"],jsonObj["組織型態"],loc,jsonObj["寺廟電話 1"],jsonObj["寺廟電話 2"])
            templeLst.append(g)

    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8-sig"))

    return render(request,
        'app/allmygods.html',
        context_instance = RequestContext(request,
        {
            'title':'求人不如求神',
            'gods':templeLst,
        }))
    
def address_to_location(request):
    assert isinstance(request, HttpRequest)
    #address = request.POST['address']
    #if address == "":
    try:
        success, lat, lng = AddressToLatlng(address)
        if  success == True:
            return HttpResponse(json.dumps({"status": "OK", "lat": lat, "lng": lng}),
            content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "Fail", "lat": lat, "lng": lng}),
            content_type="application/json")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8-sig"))
    return HttpResponse(json.dumps({"status": "Fail", "lat": lat, "lng": lng}),
                        content_type="application/json")

def AddressToLatlng(address):
    encodeAddress = urllib.parse.urlencode({'address': address})
    url = "https://maps.googleapis.com/maps/api/geocode/json?%s" % encodeAddress
    req = Request(url)
    response = urllib.request.urlopen(req).readall().decode('utf-8')
    jsongeocode = json.loads(response) 
    longitude = 0.0
    latitude = 0.0
    success = False

    if  jsongeocode['status'] == "OK":
        success = True
        longitude, latitude = jsongeocode['results'][0]['geometry']['location'].values()        
    return success, latitude, longitude

@csrf_protect
def syncTempleInfo(request):
    assert isinstance(request, HttpRequest)
    req = Request("http://opendata.hccg.gov.tw/dataset/480911dd-6eea-4f97-a7e8-334b32cc8f6b/resource/ee12c072-e8aa-4be1-8179-f1c9606198f3/download/20150304091340575.json")
    templeLst = []
    success = False
    try:
        response = urllib.request.urlopen(req)
        ur = response.readall().decode('utf-8-sig')
        j_obj = json.loads(ur) 
        
        for jsonObj in j_obj:
            address = jsonObj["寺廟所在地"]
            success, lat, lng = AddressToLatlng(address)
            if success == True:
                wgs84locate = latlng(lat, lng)
                loc = location(address,wgs84locate)
            else:
                wgs84locate = latlng(0.0, 0.0)
                loc = location(address,wgs84locate)

            g = temple(jsonObj["寺廟名稱"],jsonObj["地區"],jsonObj["主祀神像"],jsonObj["教別"],jsonObj["組織型態"],loc,jsonObj["寺廟電話 1"],jsonObj["寺廟電話 2"])
            templeLst.append(g)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8-sig"))

    if len(templeLst) > 0:
        # sync templeInfo to database
        for item in templeLst:
            filterResult = TempleInfo.objects.filter_temple(name = item.name, locateRegion = item.locateRegion, masterGod = item.mastergod)
            if len(filterResult) == 0:
                templeItem = TempleInfo.objects.create_temple(name=item.name, locateRegion=item.locateRegion, religiousBelief=item.religiousBelief,
                                                                masterGod=item.mastergod, address=item.location.address, latitude=item.location.latlng.lat,
                                                                longitude=item.location.latlng.lng, phone1=item.phone1, phone2=item.phone2)
            elif len(filterResult) == 1 and filterResult[0].latitude == 0 and filterResult[0].longitude == 0 :
                latitude = item.location.latlng.lat 
                longitude = item.location.latlng.lng
                if latitude != 0 and longitude != 0:
                    filterResult[0].latitude = latitude
                    filterResult[0].longitude = longitude
                    filterResult[0].save()


        return HttpResponse(json.dumps({"status": "Success"}),
                        content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "Fail"}),
                        content_type = "application/json")
