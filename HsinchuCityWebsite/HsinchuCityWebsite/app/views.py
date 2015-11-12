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
from app.models import god
from django.contrib.sites import requests

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

def allMyGods(request):
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/allmygods.html',
        context_instance = RequestContext(request,
        {
            'title':'求人不如求神',
        }))

def allMyGodsInHsinchu(request):
    assert isinstance(request, HttpRequest)
    req = Request("http://opendata.hccg.gov.tw/dataset/480911dd-6eea-4f97-a7e8-334b32cc8f6b/resource/ee12c072-e8aa-4be1-8179-f1c9606198f3/download/20150304091340575.json")
    try:
        response = urllib.request.urlopen(req)
        ur = response.readall().decode('utf-8-sig')
        j_obj = json.loads(ur) 
        templeLst = []
        for jsonObj in j_obj:
            g = god(jsonObj["寺廟名稱"],jsonObj["地區"],jsonObj["主祀神像"],jsonObj["教別"],jsonObj["組織型態"],jsonObj["寺廟所在地"],jsonObj["寺廟電話 1"],jsonObj["寺廟電話 2"])
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
    address = request.GET['address']
    encodeAddress = urllib.parse.urlencode({'address': address})
    url = "https://maps.googleapis.com/maps/api/geocode/json?%s" % encodeAddress
    try:
        req = Request(url)
        response = urllib.request.urlopen(req).readall().decode('utf-8')
        jsongeocode = json.loads(response) 
        if  jsongeocode['status'] == "OK":
            longitude, latitude = jsongeocode['results'][0]['geometry']['location'].values()
        else:
            return HttpResponse(json.dumps({"status": "Fail"}),
            content_type="application/json")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf-8-sig"))    
    return HttpResponse(json.dumps({"status": "OK", "lat": latitude, "lng": longitude}),
            content_type="application/json")
