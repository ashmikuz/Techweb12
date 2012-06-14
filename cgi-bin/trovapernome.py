#!/usr/bin/python
# -*- coding: utf-8 -*-

import error
import urllib2
import urllib
import cgi

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr").lower()
    name=fs.getvalue("name").lower()
    if (not name or not aggr):
        error.errhttp("406");
    else:
        urldescr="http://ltw1219.web.cs.unibo.it/trova-per-nome/"+aggr+"/params/"+name
        urldescr=urllib.quote(urldescr,  safe="%/:=&?~#+!$,;'@()*[]")
        req=urllib2.Request(url=urldescr)
        req.add_header('Accept', 'application/xml')
        response = urllib2.urlopen(req)
        resource=response.read()
        response.close()
        print ("Content-type: text/plain; charset=UTF-8\n")
        print resource
        
main()