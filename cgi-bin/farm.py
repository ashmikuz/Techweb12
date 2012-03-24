#!/usr/bin/python

import cgi
import os
import string


def main():
    fs = cgi.FieldStorage()
    accept=os.environ["HTTP_ACCEPT"]
    if("key" not in fs) and ("comp" not in fs) and ("value" not in fs):
        if(string.find(accept, "application/xml")):
            xml=open("../data/farmacieBO2011.xml", "r")
            print("Content-type: application/xml; charset=UTF-8\n")
            content=xml.read()
            print content
    else:
        print os.environ["HTTP_USER_AGENT"]
        print os.environ["REQUEST_METHOD"]
        print "qstring=", os.environ["QUERY_STRING"]
        print os.environ["HTTP_ACCEPT"]


main()
