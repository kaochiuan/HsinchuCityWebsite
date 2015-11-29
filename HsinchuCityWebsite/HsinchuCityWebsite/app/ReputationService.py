# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import time

class ReputationService(object):
    def __init__(self, json_content):
        self.__json_content = json.loads(json_content) 
        self.__blogs  = {"yam":0, "pixnet": 0, "xuite": 0, "blogspot": 0, "ptt": 0}
        self.__google_search =  "https://www.google.com/search"
        self.__reputation_keywords = {"推薦":1, "溫柔":1, "讚":1, "不要去":-1, "不推薦":-1, "不推":-1, "抱怨":-1}

    def get_animal_hospitals(self):
        #with open(self.__hospital_data_file) as f:
        #    data = json.load(f)
        data = self.__json_content
        addresses = [data[i][u"機構地址"] for i in range(len(data))]        
        coordinates = list(map(lambda address: self.address_to_location(address), addresses))  
        hospitals = {data[i][u"機構名稱"]:coordinates[i] for i in range(len(data))}
        return hospitals

    def address_to_location(self, address):
        api = "http://maps.googleapis.com/maps/api/geocode/json"
        qs = {"address": address, "sensor": "false"}
        success = True
        time.sleep(0.2)
        r = requests.get(api, params=qs)
        data = r.json()

        try:
            latitude, longitude  =  data['results'][0]['geometry']['location'].values()
        except Exception:
            success = False
            longitude, latitude = [0,0]
        return (success, longitude, latitude)

    def links_crawler(self, keywords):
        qs = {"q": keywords}
        r = requests.get(self.__google_search, params=qs)
        htext = r.text

        soup = BeautifulSoup(htext, "html.parser")
        search = soup.findAll('div', attrs={'id': 'search'})
        searchtext = str(search[0])
        items = BeautifulSoup(searchtext, "html.parser").findAll('li')
        
        regex = "q=https?://(?!.*q).*?&amp"
        pattern = re.compile(regex)
        blog_ptn = [re.compile(key) for key in self.__blogs.keys()]
        results = []
        for item in items:
            links = BeautifulSoup(str(item), "html.parser").findAll('a')
            source_link = links[0]
            source_url = re.findall(pattern, str(source_link))
            if len(source_url) > 0:
                url = source_url[0].replace("q=", "").replace("&amp", "")
                blog_flags = list(map(lambda ptn: len(re.findall(ptn, url)), blog_ptn))
                if sum(blog_flags):
                    blog_category_id = blog_flags.index(1)
                    blog_category = list(self.__blogs)[blog_category_id]
                    results.append((blog_category, url))
        return results

    def get_hospital_links(self, hospitals):
        result = {}
        for name in hospitals:
            links = []

            links = self.links_crawler(name)
            result.update({name:links})
        return result

    def blog_crawler_by_title(self, hospital_link_data):
        result = {}
        for k, v in hospital_link_data.items():
            if len(v):
                data = list(map(self.get_blog_title, v))
                data = "".join(data)
            else:
                data = ""
            
            if not k in result:
                result.update({k:data})

#            fname = "./data/"+ k + ".txt"
#            with open(fname, 'wb+') as f:
#                f.write(data+"\n")

        return result

    def get_blog_title(self, blog_data):
        blog_category = blog_data[0]
        link = blog_data[1]

        r = requests.get(link)
        if r.encoding == 'ISO-8859-1': # 'big5'
            r.encoding = 'utf-8'
        htext = r.text
        soup = BeautifulSoup(htext, "html.parser")
        search = []
        if blog_category in self.__blogs:
            search = soup.findAll('title')     
        blog_data = [re.sub("<.*?>", "", str(k)) for k in search]
        blog_data = "".join(blog_data)   
        return blog_data
    
    def calculate_reputation_score(self, text):
        keyword_ptn = [re.compile(key) for key in self.__reputation_keywords.keys()]
        reputations = list(map(lambda ptn: len(re.findall(ptn, text)), keyword_ptn))
        indices = [i for i, x in enumerate(reputations) if x > 0]
        ky = list(map(lambda id: list(self.__reputation_keywords)[id], indices))
        scores = list(map(lambda key: self.__reputation_keywords[key], ky))
        score = sum(scores)
        return score

    def get_reputation(self, hospitals, blog_text_data):
        reputation = {k:(v, self.calculate_reputation_score(blog_text_data[k])) for k, v in hospitals.items()}
        return reputation

#if __name__ == '__main__':
#    ahr = ReputationService("./animals.json")
#    hos = ahr.get_animal_hospitals()
#    links = ahr.get_hospital_links(hos.keys()) # name: ((success, longitude, latitude),score)
#    data = ahr.blog_crawler_by_title(links)
#    rep = ahr.get_reputation(hos, data)

#    for k, v in rep.iteritems():
#        print k, v



