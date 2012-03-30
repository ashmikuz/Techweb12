#!/usr/bin/python

def geterrstring(errno):
    if(errno=="403"):
        return "Forbidden"
    if(errno=="404"):
        return "Not found"
    if(errno=="405"):
        return "Method not allowed"
    if(errno=="406"):
        return "Not acceptable"
    if(errno=="500"):
        return "Internal server error"

def errhttp(errno):
    print "Status:",errno,geterrstring(errno),"\n";
    return