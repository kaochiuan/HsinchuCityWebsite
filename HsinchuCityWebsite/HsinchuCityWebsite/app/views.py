﻿"""
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
from app.models import TempleInfo, TempleManager, CultureActiviyInfo, CityNewsItem
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
            'title':'首頁',
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
            'title':'Settings',
            'message':'Application data sync',
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
    data = serializers.serialize("json", filterTemples, fields=('name','masterGod','address','latitude','longitude'))

    decoded = json.loads(data)
    return HttpResponse(json.dumps({"status": "Success", "templeInfo": decoded}),
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
        latitude, longitude = jsongeocode['results'][0]['geometry']['location'].values()        
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

@csrf_protect
def syncCultureInfo(request):
    assert isinstance(request, HttpRequest)
    req = Request("http://opendata.hccg.gov.tw/dataset/28f1cd76-59b9-4877-b350-b064db635eb8/resource/82c2be17-0593-429b-842b-409735a9860f/download/20151119195903997.json")
    activityLst = []
    success = False
    try:
        response = urllib.request.urlopen(req)
        ur = response.readall().decode('utf-8-sig')
        j_obj = json.loads(ur) 
        for jsonObj in j_obj:
            address = jsonObj["地點地址"]
            success, lat, lng = AddressToLatlng(address)
            if success == True:
                wgs84locate = latlng(lat, lng)
                loc = location(address,wgs84locate)
            else:
                wgs84locate = latlng(0.0, 0.0)
                loc = location(address,wgs84locate)

            activity = cultureActiviy(jsonObj["活動主題"],jsonObj["起始日"],jsonObj["截止日"],jsonObj["時間"],jsonObj["活動名稱"],jsonObj["地點"],loc)
            activityLst.append(activity)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8-sig"))

    if len(activityLst) > 0:
        # sync CultureActiviyInfo to database
        for item in activityLst:
            filterResult = CultureActiviyInfo.objects.filter_activity(name = item.name,activityTheme = item.activityTheme, locationName = item.locationName,
                                                                      address = item.location.address, startDate = item.startDate, endDate = item.endDate)
                                                                      
            if len(filterResult) == 0:
                templeItem = CultureActiviyInfo.objects.create_activity(name=item.name, activityTheme=item.activityTheme,locationName= item.locationName,
                                                                        address=item.location.address, latitude=item.location.latlng.lat, longitude=item.location.latlng.lng,
                                                                        startDate = item.startDate, endDate = item.endDate, activityTime = item.time)
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

@csrf_protect
def syncCityNews(request):
    assert isinstance(request, HttpRequest)
    req = Request("http://opendata.hccg.gov.tw/dataset/e9443b8a-da93-46a9-b794-49aabbb815fd/resource/0f3f2cb2-2552-44bf-ba08-54dfaafda034/download/20151127133908155.json")
    newsLst = []
    success = False
    try:
        response = urllib.request.urlopen(req)
        ur = response.readall().decode('utf-8-sig')
        j_obj = json.loads(ur) 

        for jsonObj in j_obj:
            start = TaiwanDateToStdDate(jsonObj["發布起始日期"])
            end = TaiwanDateToStdDate(jsonObj["發布截止日期"])
            news = cityNewes(jsonObj["標題"],start,end,jsonObj["類別"],jsonObj["內容"],jsonObj["圖片路徑(1)"])
            newsLst.append(news)

    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8-sig"))

    if len(newsLst) > 0:
        # sync CityNewsItem to database
        for item in newsLst:
            filterResult = CityNewsItem.objects.filter_news(title = item.title, type = item.type, publishDate = item.publishDate, endDate = item.endDate)
                                                                      
            if len(filterResult) == 0:
                templeItem = CityNewsItem.objects.create_news(title = item.title, type = item.type,content = item.content, publishDate = item.publishDate, 
                                                              endDate = item.endDate, picturePath = item.picturePath)
            elif len(filterResult) == 1 :
                 filterResult[0].content = item.content
                 filterResult[0].picturePath = item.picturePath
                 filterResult[0].save()
        return HttpResponse(json.dumps({"status": "Success"}),
                        content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status": "Fail"}),
                        content_type = "application/json")

def cultureActivities(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/cultureActivities.html',
        context_instance = RequestContext(request,
        {
            'title':'當月藝文活動',
            'year':datetime.now().year,
        }))

def cityNews(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/cityNews.html',
        context_instance = RequestContext(request,
        {
            'title':'市府新聞',
            'year':datetime.now().year,
        }))

def TaiwanDateToStdDate(dateStr):    
    return datetime.strptime(dateStr, "%Y%m%d")

@csrf_protect
def filterCultureActivities(request):
    assert isinstance(request, HttpRequest)
    keyword = request.POST['keyword']

    filterActivities = CultureActiviyInfo.objects.filterByKeyword(keyword)
    data = serializers.serialize("json", filterActivities, fields=('name','activityTheme',
                                                                   'address','latitude','longitude',
                                                                   'locationName','startDate','endDate','activityTime'))

    decoded = json.loads(data)
    return HttpResponse(json.dumps({"status": "Success", "activityInfo": decoded}),
                        content_type="application/json")

@csrf_protect
def getTop10News(request):
    assert isinstance(request, HttpRequest)
    topNews = CityNewsItem.objects.TopNews()
    data = serializers.serialize("json", topNews, fields=('title','type','content',
                                                          'publishDate','picturePath'))

    decoded = json.loads(data)
    return HttpResponse(json.dumps({"status": "Success", "news": decoded}),
                        content_type="application/json")