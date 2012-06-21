#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from math import radians, sqrt, atan2, cos, fabs, sin, pow
from costanti import uencoding, csvfields, weekdays, months
import error
import csv
import json
import codecs
import datetime
sys.path.append("/home/web/ltw1218/cgi-bin/libs/")
from lxml import etree
from collections import OrderedDict
from StringIO import StringIO
import rdflib
from rdflib import plugin
from rdflib.graph import ConjunctiveGraph as Graph
from rdflib.namespace import Namespace, XSD
from rdflib.term import Literal
import rdfextras
import datetime


raggioterra=float(6371009)

dial=csv.Dialect
dial.quoting=csv.QUOTE_ALL
dial.quotechar='"'
dial.delimiter=","
dial.lineterminator="\n"
dial.escapechar="\\"

query="""
                PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
                PREFIX cs: <http://cs.unibo.it/ontology/>
                PREFIX : <http://www.essepuntato.it/resource/>

                SELECT ?id ?name ?lat ?long ?tel ?category ?fax ?opening ?closing ?address
                WHERE {
                        ?id vcard:category ?category ;
                        vcard:fn ?name ;
                        vcard:extended-address ?address ;
                        vcard:latitude ?lat ;
                        vcard:longitude ?long ;
                        vcard:tel ?tel ;
                        vcard:fax ?fax ;
                        cs:opening ?opening ;
                        cs:closing ?closing .
                }
        """
        
meta_query="""
                PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
                PREFIX cs: <http://cs.unibo.it/ontology/>
                PREFIX : <http://www.essepuntato.it/resource/>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX this: <http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl#>
                SELECT ?creator ?created ?description ?valid ?source
                WHERE {
                        this:metadata dcterms:creator ?creator;
                        dcterms:created ?created;
                        dcterms:description ?description ;
                        dcterms:valid ?valid ;
                        dcterms:source ?source.
                }
        """
        
plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')


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
    def aperto(self, opening):
        if opening.lower() in weekdays:
            if opening in self.opening.lower():
                return True
            else:
                return False
        else:
            datelist=opening.split("-")
            now = datetime.datetime.now()
            if(len(datelist)==2):
                    year=str(now.year)
                    day=datelist.pop()
                    month=datelist.pop()
                    date=datetime.date(int(year),int(month),int(day))
            elif(len(datelist)==3):
                    
                    day=datelist.pop()
                    month=datelist.pop()
                    year=datelist.pop()
                    date=datetime.date(int(year),int(month),int(day))
            else:
                    return 404
            if("%s-%s-%s" % (year,month,day) in self.opening or "%s-%s" % (month,day) in self.opening):
                return True
            elif ("%s-%s-%s" % (year,month,day) in self.closing or "%s-%s" % (month,day) in self.closing):
                return False
            elif (str(date.day)+" "+months[date.month - 1] in self.closing.lower()):
                return False
            elif(weekdays[date.weekday()] in self.opening.lower()):
                return True
            elif(str(date.day)+" "+months[date.month - 1] in self.opening.lower()):
                return True
            else:
                return False

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
    for key,value in orig.iteritems():
        for subkey,subval in value.iteritems():
            if(key=="metadata"):
                creator=value["creator"]
                created=value["created"]
                valid=value["valid"]
                version=value["version"]
                source=value["source"]
                meta=metadata(creator,created,version,source,valid)
            else:
             	id=subkey
                category=subval["category"][0]
                if (len(subval["category"])==2):
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

def locationfromturtle(data,loclist):
    turtle=rdflib.Graph()
    src=turtle.parse(StringIO(data), format='n3')
    src.bind('', rdflib.URIRef('http://www.essepuntato.it/resource/', False))
    src.bind('vcard', rdflib.URIRef('http://www.w3.org/2006/vcard/ns#'))
    src.bind('cs', rdflib.URIRef('http://cs.unibo.it/ontology/'))
    src.bind('dcterms', rdflib.URIRef('http://purl.org/dc/terms/'))
    src.bind('xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))
    src.bind('this', rdflib.URIRef('http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl#'))
    query_result=src.query(query)
    meta_result=src.query(meta_query)
    for element in query_result:
        id=element[0].split("/")
        id=id[-1]
        name=element[1]
        lat=element[2]
        long=element[3]
        tel=element[4]
        category=element[5]
        fax=element[6]
        opening=element[7]
        closing=element[8]
        address=element[9]
        subcategory=""
        note=""
        loc=location(id, category, subcategory,name, lat, long, address, opening, closing, tel, note)
        loclist.append(loc)
    for metaelement in meta_result:
        creator=metaelement[0]
        created=metaelement[1]
        version=metaelement[2]
        valid=metaelement[3]
        source=metaelement[4]
        meta=metadata(creator,created,version,source,valid)
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
        print str
        
def locationtoturtle(ellist, meta):
    rdf=Graph();
    cs = Namespace("http://cs.unibo.it/ontology/")
    colon=Namespace("http://www.essepuntato.it/resource/")
    dcterms=Namespace("http://purl.org/dc/terms/")
    xsd=Namespace("http://www.w3.org/2001/XMLSchema#")
    this=Namespace("http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl#")
    vcard = Namespace("http://www.w3.org/2006/vcard/ns#")
    rdf.bind("vcard", vcard)
    rdf.bind("cs", cs)
    rdf.bind("", colon)
    rdf.bind("dcterms", dcterms)
    rdf.bind("xsd", xsd)
    rdf.bind("this", this)
    rdf.add((this["metadata"], dcterms["creator"], Literal(meta.creator)))
    rdf.add((this["metadata"], dcterms["created"], Literal(meta.created,datatype=XSD.date)))
    rdf.add((this["metadata"], dcterms["description"], Literal(meta.version)))
    rdf.add((this["metadata"], dcterms["valid"], Literal(meta.valid,datatype=XSD.date)))
    rdf.add((this["metadata"], dcterms["source"], Literal(meta.source)))
    for location in ellist:
        rdf.add((colon[location.id], vcard["fn"], Literal(location.name)))
        rdf.add((colon[location.id], vcard["extended-address"], Literal(location.address)))
        rdf.add((colon[location.id], vcard["category"], Literal(location.category)))
        rdf.add((colon[location.id], vcard["latitude"], Literal(location.lat)))
        rdf.add((colon[location.id], vcard["longitude"], Literal(location.long)))
        if(location.tel):
            rdf.add((colon[location.id], vcard["tel"], Literal(location.tel)))
        if(location.note):
            rdf.add((colon[location.id], vcard["note"], Literal(location.note)))
        rdf.add((colon[location.id], cs["opening"], Literal(location.opening)))
        rdf.add((colon[location.id], cs["closing"], Literal(location.closing)))
    print("Content-type: text/turtle; charset=UTF-8\n")
    print rdf.serialize(format="n3")
        
        

def formatresult(mimetype, ellist,meta):
    if ("application/xml" in mimetype or "*/*" in mimetype):  
        locationtoxml(ellist,meta)
    elif("application/json" in mimetype):
        locationtojson(ellist,meta)
    elif("text/csv" in mimetype):
        locationtocsv(ellist,meta)
    elif("text/turtle" in mimetype):
        locationtoturtle(ellist,meta)
    else:
        error.errhttp("406")

        