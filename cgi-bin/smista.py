#!/usr/bin/python

import cgi
import os
import xml.etree
import xml.dom.minidom
import libxml2


campi=cgi.FieldStorage()
if "aggr" not in campi:
    print "Content-Type: text/plain\n"
    print 
    print "404"

else:
    aggrno=campi.getvalue("aggr")
    print "Content-Type: text/plain\n"
    print aggrno