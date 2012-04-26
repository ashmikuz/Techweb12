#!/usr/bin/python
# -*- coding: utf-8 -

import cgi
import error
import codecs
import urllib2
import os
import trasforma

headers={'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'}

loclist=[]

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr")
    lat=fs.getvalue("lat")
    longi=fs.getvalue("long")
    maxel=fs.getvalue("maxel")
    if ((not aggr) or (not lat) or (not longi)):
        error.errhttp("406")
    else:
        """urlaggr=getaggrurl(aggr)"""
        urlaggr="http://ltw1218.web.cs.unibo.it/ltw1218-farmacie"
        req=urllib2.Request(url=urlaggr)
        req.add_header('Accept', 'application/xml, text/turtle, text/csv, application/json')
        response = urllib2.urlopen(req)
        restype= response.info().gettype()
        resource=response.read()
        response.close()
        if(restype=="application/xml"):
            print("Content-type: text/plain; charset=UTF-8\n")
            trasforma.locationfromxml(resource,loclist)
        elif(restype=="text/turtle"):
            trasforma.locationfromturtle(resource,loclist)
        elif(restype=="text/csv"):
            trasforma.locationfromcsv(resource,loclist)
        elif(restype=="application/json"):
            trasforma.locationfromcsv(resource,loclist)
        else:
            error.errhttp("406")
        computedistances(loclist, lat, longi)
        loclist.sort(key=lambda location: location.distance)
        trasforma.formatresult(os.environ["HTTP_ACCEPT"], loclist)
        
def computedistances(list, lat, longi):
    for location in list:
        location.distance(float(lat),float(longi))
        
main()