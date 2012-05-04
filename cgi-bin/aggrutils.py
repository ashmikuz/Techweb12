#!/usr/bin/python
# -*- coding: utf-8 -

import os
import os.path
from lxml import etree
import urllib2
import time
from costanti import metacat, uencoding

def isnotupdated(lastedit):
    return (time.time() - 86400 > lastedit)
    

def getaggrurl(name):
    if(True or isnotupdated(os.path.getmtime("../data/aggrcache.xml"))):
        updateaggrcache()
    xml=etree.parse("../data/aggrcache.xml")
    result=xml.xpath("/aggregatori/aggregatore[@id=\""+name+"\"]")
    if(result is None):
        return 404
    return result.pop().attrib["url"]

def updateaggrcache():
    metaccontent = urllib2.urlopen(metacat)
    data=metaccontent.read()
    cataloghi=etree.fromstring(data)
    rss=cataloghi.xpath("/metaCatalogo/catalogo/@url")
    aggrcache=etree.Element("aggregatori")
    for caturl in rss:
        try:
            catreq= urllib2.urlopen(caturl)
        except:
            continue
        cdata=catreq.read()
        try:
            catxml=etree.fromstring(cdata)
        except:
            continue
        aggregatori=catxml.xpath("/catalogo/aggregatori/aggregatore")
        for item in aggregatori:
            aggrcache.append(item)
    file=open("../data/aggrcache.xml","w")
    file.write(etree.tostring(aggrcache,pretty_print=True,encoding=uencoding))
        