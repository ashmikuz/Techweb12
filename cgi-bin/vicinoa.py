#!/usr/bin/python
# -*- coding: utf-8 -

import cgi
import error
import codecs
import urllib2
import os
from trasforma import ellist
import trasforma

headers={'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'}

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
            trasforma.locationfromxml(resource)
        elif(restype=="text/turtle"):
            trasforma.locationfromturtle(resource)
        elif(restype=="text/csv"):
            trasforma.locationfromcsv(resource)
        elif(restype=="application/json"):
            trasforma.locationfromcsv(resource)
        else:
            error.errhttp("406")
        computedistances(ellist, lat, longi)
        ellist.sort(key=lambda location: location.distance)
        trasforma.formatresult(os.environ["HTTP_ACCEPT"])
        
def computedistances(list, lat, longi):
    for location in list:
        location.distance()
        
main()