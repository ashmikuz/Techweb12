#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import error
import codecs
import trasforma
import os
import urllib2
import operator
from trasforma import metadata
from aggrutils import getaggrurl



finallist=[]
loclist=[]

ops = {
  "and": operator.and_,
  "or": operator.or_,
  "not": operator.not_
  }


def matchesoperator(datelist, operatore, location):
    boollist=[]
    xoraux=False
    if(operatore=="and" or operatore=="not"):
        result=True
    elif(operatore=="or" or operatore=="xor"):
        result=False
    else:
        return 406
    for date in datelist:
        boollist.append(location.aperto(date))
    for item in boollist:
        if(operatore=="xor"):
            if(item):
                if(xoraux):
                    return False
                xoraux=True
        elif(operatore=="not"):
            result=result and not item
        else:
            result=ops[operatore](result, item)
    return result
            
            
def getopened(dates, operator,loclist):
    datelist=dates.split("/")
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
        meta=trasforma.locationfromjson(resource,loclist)
    else:
        error.errhttp("406")
    finallist=getopened(dates, operator,loclist)
    if(isinstance(finallist, ( int, long ))):
        error.errcode(str(finallist))
        return
    trasforma.formatresult(os.environ["HTTP_ACCEPT"], finallist, meta)

main()

