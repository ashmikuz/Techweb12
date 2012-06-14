#!/usr/bin/python
# -*- coding: utf-8 -*-

import error
import urllib2
import urllib
import cgi

def main():
    fs = cgi.FieldStorage()
    multiint=fs.getvalue("multi")
    intsemplice=fs.getvalue("simple")
    if (not multiint or not intsemplice):
        error.errhttp("406");
    else:
        urldescr="http://ltw1219.web.cs.unibo.it/aperto/params/"+multiint+"/"+intsemplice
        urldescr=urllib.quote(urldescr,  safe="%/:=&?~#+!$,;'@()*[]")
        req=urllib2.Request(url=urldescr)
        req.add_header('Accept', '*/*, application/xml, text/turtle, text/csv, application/json')
        response = urllib2.urlopen(req)
        restype= response.info().gettype()
        resource=response.read()
        response.close()
        print ("Content-type: text/plain; charset=UTF-8\n")
        print resource
        
        
main()