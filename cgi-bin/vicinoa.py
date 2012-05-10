#!/usr/bin/python
# -*- coding: utf-8 -

import cgi
import error
import codecs
import urllib2
import os
import trasforma
from trasforma import metadata
from aggrutils import getaggrurl

headers={'Accept': 'application/xml,application/json,text/turtle, text/csv, text/html, text/plain;'}
loclist=[]

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr")
    lat=fs.getvalue("lat")
    longi=fs.getvalue("long")
    if("maxel" in fs):
        maxel=(int(fs.getvalue("maxel")))
    else:
        maxel=None
    if ((not aggr) or (not lat) or (not longi)):
        error.errhttp("406")
        return
    urlaggr=getaggrurl(aggr)
    if(isinstance(urlaggr, ( int, long ))):
        error.errhttp(str(urlaggr))
        return
    req=urllib2.Request(url=urlaggr)
    req.add_header('Accept', 'application/xml, text/turtle, text/csv, application/json')
    response = urllib2.urlopen(req)
    restype= response.info().gettype()
    resource=response.read()
    response.close()
    if(restype=="application/xml"):
        meta=trasforma.locationfromxml(resource,loclist)
    elif(restype=="text/turtle"):
        meta=trasforma.locationfromturtle(resource,loclist)
    elif(restype=="text/csv"):
        meta=trasforma.locationfromcsv(resource,loclist)
    elif(restype=="application/json"):
        meta=trasforma.locationfromjson(resource,loclist)
    else:
        error.errhttp("406")
    computedistances(loclist, lat, longi)
    loclist.sort(key=lambda location: location.distance)
    if(maxel):
        trasforma.formatresult(os.environ["HTTP_ACCEPT"], loclist[:maxel], meta)
    else:
        trasforma.formatresult(os.environ["HTTP_ACCEPT"], loclist, meta)
        
def computedistances(list, lat, longi):
    for location in list:
        location.distance(lat,longi)
        
main()