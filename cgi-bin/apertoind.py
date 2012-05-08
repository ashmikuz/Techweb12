#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import error
import codecs
import trasforma
import os
import urllib2
from trasforma import metadata
from aggrutils import getaggrurl

loclist=[]
finallist=[]

def matchesoperator(datelist, operator, location):
    boollist=[]
    for date in datelist:
        if(location.apero(date)):
            boollist.append(location)
    

def getopened(dates, operator,loclist):
    print("Content-type: text/plain; charset=UTF-8\n")
    datelist=dates.split("/")
    loclist=filter(lambda location: location.aperto(dates), loclist)
    tobeadded=False
    for location in loclist:
        if(matchesoperator(datelist, operator, location)):
            finallist.append(location)      
    return finallist

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr").lower()
    operator=fs.getvalue("operator").lower()
    dates=fs.getvalue("dates").lower()
    if ((not aggr) or (not operator) or (not dates)):
        error.errhttp("406")
        return
    urlaggr=getaggrurl(aggr)
    if(urlaggr=="404"):
        error.errhttp("404")
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
        meta=trasforma.locationfromcsv(resource,loclist)
    else:
        error.errhttp("406")
    finallist=getopened(dates, operator,loclist)
    trasforma.formatresult(os.environ["HTTP_ACCEPT"], finallist, meta)

main()

