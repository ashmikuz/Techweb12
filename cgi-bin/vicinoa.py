#!/usr/bin/python
# -*- coding: utf-8 -

import cgi
import error
import codecs
import urllib2
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
        urlaggr=getaggrurl(aggr)
        req=urllib2.Request(url=urlaggr)
        req.add_header('Accept', 'application/xml, text/turtle, text/csv, application/json')
        response = urllib2.urlopen(r)
        restype= response.info.gettype()
        resource=response.read()
        response.close()
        if(restype=="application/xml"):
            trasforma.locationfromxml(data)
            computedistances(ellist)
            ellist.sorted(key=lambda location: location.distance)
        elif(restype=="text/turtle"):
            trasforma.locationfromturtle(data)
            computedistances(ellist)
            ellist.sorted(key=lambda location: location.distance)
        elif(restype=="text/csv"):
            trasforma.locationfromcsv(data)
            computedistances(ellist)
            ellist.sorted(key=lambda location: location.distance)
        elif(restype=="application/json"):
            trasforma.locationfromcsv(data)
            computedistances(ellist)
            ellist.sorted(key=lambda location: location.distance)
        else:
            error.errhttp("406")
        trasforma.formatresult(os.environ["HTTP_ACCEPT"])