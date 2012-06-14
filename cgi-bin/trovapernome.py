#!/usr/bin/python
# -*- coding: utf-8 -*-

import error
import urllib2
import cgi

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr").lower()
    name=fs.getvalue("name").lower()
    if (not name or not aggr):
        error.errhttp("406");
    else:
        urlaggr="http://ltw1219.web.cs.unibo.it/trova-per-nome/"+aggr+"/params/"+name
        req=urllib2.Request(url=urlaggr)
        req.add_header('Accept', 'application/xml, text/turtle, text/csv, application/json')
        response = urllib2.urlopen(req)
        restype= response.info().gettype()
        resource=response.read()
        response.close()
        print ("Content-type: application/xml; charset=UTF-8\n")
        print resource
        
        
main()