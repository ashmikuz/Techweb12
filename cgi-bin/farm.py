#!/usr/bin/python

import cgi
import os
import string
import libxml2
import urllib


def main():
    fs = cgi.FieldStorage()
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    accept=os.environ["HTTP_ACCEPT"]
    if(not chiave) and (not confronto) and (not valore):
        if(string.find(accept, "application/xml")):
            xml=open("../data/farmacieBO2011.xml", "r")
            print("Content-type: application/xml; charset=UTF-8\n")
            content=xml.read()
            print content
    else:
        if(not chiave) or (not confronto) or (not valore):
            errhttp("406")
        else:
            if(confronto=="EQ"):
                filtraEQ(chiave, valore, False)
            elif(confronto=="NEQ"):
                filtraEQ(chiave,valore,True)
            elif(confronto=="CONTAINS"):
                filtraCONTAINS(chiave,valore, False)
            elif(confronto=="NCONTAINS"):
                filtraCONTAINS(chiave,valore,True)
            elif(confronto=="GT"):
                filtraGT(chiave,valore,False)
            elif(confronto=="LT"):
                filtraGT(valore,chiave,False)
            elif(confronto=="GE"):
                filtraGT(chiave,valore,True)
            elif(confronto=="LE"):
                filtraGT(valore,chiave,True)
            

main()

def errhttp(errno):
    return

def filtraEQ(key, value, nequal):
    xml=libxml2.parseDoc((open("../data/farmacieBO2011.xml", "r").read()))
    if(key=="id") or (key=="lat,long"):
        xpath="/locations/location[@"+key+"="+value+"]"
        rss=xml.xpathEval(xpath)
        print("Content-type: application/xml; charset=UTF-8\n")
        for node in rss:
            print node
    elif(key=="name"):
        xpath="/locations/location/name[@"+key+"="+value+"]"
    return

def filtraCONTAINS(key,value,ncontains):
    return