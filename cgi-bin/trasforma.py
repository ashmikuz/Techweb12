#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from math import radians, sqrt, atan2, cos, fabs, sin, pow
from costanti import uencoding, csvfields
import error
import csv
import json
import codecs
sys.path.append("/home/web/ltw1218/cgi-bin/libs/")
from lxml import etree
from collections import OrderedDict
from StringIO import StringIO

raggioterra=float(6371009)

dial=csv.Dialect
dial.quoting=csv.QUOTE_ALL
dial.quotechar='"'
dial.delimiter=","
dial.lineterminator="\n"
dial.escapechar="\\"


class location:
    def __init__(self, id, category,subcategory, name, lat, long, address, opening, closing, tel, note):
        self.id=id
        self.category=category
        self.subcategory=subcategory
        self.name=name
        self.lat=lat
        self.long=long
        self.address=address
        self.opening=opening
        self.closing=closing
        self.tel=tel
        self.note=note
    def distance(self, lat, long):
        lat1=radians(float(self.lat))
        lat2=radians(float(lat))
        long1=radians(float(self.long))
        long2=radians(float(long))
        num1=pow(cos(lat2)*sin(fabs(long2-long1)),2)
        num2=pow((cos(lat1)*sin(lat2))-(sin(lat1)*cos(lat2)*cos(fabs(long2-long1))),2)
        den1=sin(lat1)*sin(lat2)
        den2=cos(lat1)*cos(lat2)*cos(fabs(long2 - long1))
        x=sqrt(num1+num2)
        y=den1+den2
        angle=atan2(x,y)
        self.distance=angle*raggioterra

global meta

class metadata:
    def __init__(self, creator, created, version, source, valid):
        self.creator=creator
        self.created=created
        self.version=version
        self.source=source
        self.valid=valid
      
def getopening(loc):
    result=""
    for item in loc.iter("opening"):
        result+=item.text
    return result


def locationfromxml(data,ellist):
    xml=etree.fromstring(data)
    res=xml.xpath("/locations/location")
    metad=xml.xpath("/locations/metadata")
    creator=metad[0].find("creator").text
    created=metad[0].find("created").text
    version=metad[0].find("version").text
    source=metad[0].find("source").text
    valid=metad[0].find("valid").text
    meta=metadata(creator,created, version,source,valid)
    for element in res:
        attr=element.attrib
        id=attr["id"]
        if(element.find("subcategory")is not None):
            subcategory=(element.find("subcategory").text)
        else:
            subcategory=""
        category=(element.find("category").text)
        name=(element.find("name").text)
        lat=(attr["lat"])
        long=(attr["long"])
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
        loc=location(id, category,subcategory ,name, lat, long, address, opening, closing, tel, note)
        ellist.append(loc)
    return meta

def locationfromjson(data,ellist):
    orig=json.loads(data)
    ellist=[]
    for key,value in orig.iteritems():
        for subkey,subval in value.iteritems():
            if(key!="metadata"):
                id=subkey
                category=subval["category"][0]
                if len(subval["category"]==2):
                    subcategory=subval["category"][1]
                else:
                    subcategory=""
                name=subval["name"]
                lat=(subval["lat"])
                long=(subval["long"])
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
                loc=location(id, category,subcategory, name, lat, long, address, opening, closing, tel, note)
                ellist.append(loc)
            else:
             	creator=value["creator"]
             	created=value["created"]
             	valid=value["valid"]
             	version=value["version"]
             	source=value["source"]
             	meta=metadata(creator,created,version,source,valid)
	return meta
             	

def locationfromcsv(data,loclist):
    orig=csv.DictReader(StringIO(data))
    donemetad=False
    for item in orig:
     	if(donemetad!=True):
			 creator=item["Creator"]
			 created=item["Created"]
			 valid=item["Valid"]
			 version=item["Version"]
			 source=item["Source"]
			 donemetad=True
			 meta=metadata(creator,created,version,source,valid)
        id=item["Id"]
        category=item["Category"]
        subcategory=item["subcategory"]
        name=item["Name"]
        lat=(item["Lat"])
        long=(item["Long"])
        address=item["Address"]
        opening=item["Opening"]
        closing=item["Closing"]
        if ("Tel" in item):
            tel=item["Tel"]
        else:
            tel=""
        if ("note" in item):
            note=item["note"]
        else:
            note=""
        loc=location(id, category, subcategory,name, lat, long, address, opening, closing, tel, note)
        loclist.append(loc)
    return meta

def locationtoxml(ellist,meta):
    root=etree.Element("locations")
    md=etree.SubElement(root,"metadata")
    submd=etree.SubElement(md,"creator")
    submd.text=meta.creator
    submd=etree.SubElement(md,"created")
    submd.text=meta.created
    submd=etree.SubElement(md,"version")
    submd.text=meta.version
    submd=etree.SubElement(md,"source")
    submd.text=meta.source
    submd=etree.SubElement(md,"valid")
    submd.text=meta.valid
    for location in ellist:
        child=etree.SubElement(root,"location" , lat=location.lat, id=location.id, long=location.long)
        subchild=etree.SubElement(child, "category")
        subchild.text=location.category
        if(location.subcategory!=""):
            subchild=etree.SubElement(child, "subcategory")
            subchild.text=location.subcategory
        subchild.text=location.category
        subchild=etree.SubElement(child, "name")
        subchild.text=location.name
        subchild=etree.SubElement(child, "address")
        subchild.text=location.address
        subchild=etree.SubElement(child, "closing")
        subchild.text=location.closing
        subchild=etree.SubElement(child, "opening")
        subchild.text=location.opening
        if(location.note!=""):
            subchild=etree.SubElement(child, "note")
            subchild.text=location.note
        if(location.tel):
            subchild=etree.SubElement(child, "tel")
            subchild.text=location.tel
    print("Content-type: application/xml; charset=UTF-8\n")
    print etree.tostring(root, pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE locations SYSTEM "http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DTDs/locations.dtd">',  encoding=uencoding)
    return

def locationtojson(ellist, meta):
    md={}
    md["creator"]=meta.creator
    md["created"]=meta.created
    md["version"]=meta.version
    md["source"]=meta.source
    md["valid"]=meta.valid
    root= {"locations" : OrderedDict(),
		  	"metadata" : md}
    for location in ellist:
        cur={}
        cur.update({"name": location.name})
        cur.update({"category" : []})
        cur["category"].append(location.category)
        if(location.subcategory!=""):
            cur["category"].append(location.subcategory)
        cur.update({"address" : location.address})
        cur.update({"lat" : location.lat})
        cur.update({"long" : location.long})
        cur.update({"opening": location.opening})
        cur.update({"closing" : location.closing})
        if(location.note!=""):
            cur.update({"note" : location.note})
        if(location.tel!=""):
            cur.update({"tel" : location.tel})
        root["locations"].update({location.id : cur})
    print("Content-type: text/plain; charset=UTF-8\n")
    print json.dumps(root, ensure_ascii=False, encoding=uencoding ,sort_keys=False, indent=4).encode(uencoding)            
    return

def locationtocsv(ellist,meta):
    print("Content-type: text/csv; charset=UTF-8\n")
    print csvfields
    for location in ellist:
        str= "\""+location.id+"\",\""+location.category+"\",\""+location.name+"\",\""+location.address+"\",\""+location.lat+"\",\""+location.long+"\",\""+location.subcategory+"\",\""+location.note+"\",\""+location.opening+"\",\""+location.closing+"\",\""+meta.creator+"\",\""+meta.created+"\",\""+meta.valid+"\",\""+meta.source+"\""
        str=str.decode(uencoding)
        print str.encode(uencoding)

def formatresult(mimetype, ellist,meta):
    if (False and "application/xml" in mimetype):  
        locationtoxml(ellist,meta)
    elif(False and "application/json" in mimetype):
        locationtojson(ellist,meta)
    elif(True or "text/csv" in mimetype):
        locationtocsv(ellist,meta)
    elif("text/turtle" in mimetype):
        locationtoturtle(ellist,meta)
    else:
        error.errhttp("406")

        