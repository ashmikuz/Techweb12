#!/usr/bin/python

import cgi
import os


def main():
    fs = cgi.FieldStorage()
    print "Content-type: text/plain\n"
    print os.environ["HTTP_USER_AGENT"]
    print os.environ["REQUEST_METHOD"]
    print "qstring=", os.environ["QUERY_STRING"]
    print os.environ["HTTP_ACCEPT"]


main()
