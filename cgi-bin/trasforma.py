#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from math import radians, sqrt, atan2, cos, abs, sin, pow
import csv
import json
sys.path.append("/home/web/ltw1218/cgi-bin/libs/")
from lxml import etree

raggioterra=float(6371000)

class location:
    def __init__(self, id, category, name, lat, long, address, opening, closing, tel, note):
        self.id=id
        self.category=category
        self.name=name
        self.lat=lat
        self.long=long
        self.address=address
        self.opening=opening
        self.closing=closing
        self.tel=tel
        self.note=note
    def distance(self, lat, long):
        lat1=radians(self.lat)
        lat2=radians(lat)
        long1=radians(self.long)
        long2=radians(long)
        x=sqrt((cos(lat2)*(pow(sin(abs(long2-long1)),2)))+pow(cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(abs(long2 - long1)),2))
        y=sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(abs(long2 - long1))
        angle=atan2(x,y)
        self.distance=angle*raggioterra
        
        

global ellist  
      
def getopening(loc):
    result=""
    for item in loc.iter("opening"):
        result+=item.text
    return result


def locationfromxml(data):
    xml=etree.parse(data)
    res=xml.xpath("/locations/location")
    ellist=[]
    for element in res:
        attr=element.attrib
        id=attr["id"]
        category=(element.find("category").text)
        name=(element.find("name").text)
        lat=float(attr["lat"])
        long=float(attr["long"])
        address=(element.find("address").text)
        opening=getopening(element)
        closing=(element.find("closing").text)
        if(element.find("tel")is not None):
            tel=(element.find("tel").text)
        else:
            tel=""
        if(element.find("note") is not None):
            note=(element.find("note").text)
        else:
            note=""
        loc=location(id, category, name, lat, long, address, opening, closing, tel, note)
        ellist.append(loc)

def locationfromjson(data):
    orig=json.loads(data)
    ellist=[]
    for key,value in orig.iteritems():
        for subkey,subval in value.iteritems():
            if(key!="metadata"):
                id=subkey
                category=[]
                for item in subval["category"]:
                    category.append(item)
                name=subval["name"]
                lat=float(subval["lat"])
                long=float(subval["long"])
                address=subval["address"]
                opening=subval["opening"]
                closing=subval["closing"]
                if("tel" in subval):
                    tel=(subval["tel"])
                else:
                    tel=""
                if("note" in subval):
                    note=subval["note"]
                else:
                    note=""
                loc=location(id, category, name, lat, long, address, opening, closing, tel, note)
                ellist.append(loc)

def locationfromcsv(data):
    orig=csv.DictReader(data)
    for item in orig:
        id=item["Id"]
        category=item["Category"]
        name=item["Name"]
        lat=float(item["Lat"])
        long=float(item["Long"])
        address=item["Address"]
        opening=item["Opening"]
        closing=item["Closing"]
        if ("Tel" in item):
            tel=item["Tel"]
        else:
            tel=""
        if ("Note" in item):
            note=item["note"]
        else:
            note=""
        loc=location(id, category, name, lat, long, address, opening, closing, tel, note)
        ellist.append(loc)
    


        