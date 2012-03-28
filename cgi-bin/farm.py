#!/usr/bin/python

import cgi
import os
import string
import libxml2
import urllib

def filtraEQ(key, value, nequal):
    if(nequal):
        operand="!="
    else:
        operand="="
    xml=libxml2.parseFile("../data/farmacieBO2011.xml")
    if(key=="id") or (key=="lat,long"):
        xpath="/locations/location[@"+key+operand+"\'"+value+"\']"
    else:
        xpath="/locations/location["+key+operand+"\'"+value+"\']"
    rss=xml.xpathEval(xpath)
    metad=xml.xpathEval("/locations/metadata")
    print("Content-type: application/xml; charset=UTF-8\n")
    print("<locations>")
    print metad[0]
    for node in rss:
        print node
    print("</locations>")
    return
    
def filtraGT(key,value,greaterthan, equal):
    if(greaterthan):
        operand=">"
    else:
        operand="<"
    if(equal):
        operand+="="
    xml=libxml2.parseFile("../data/farmacieBO2011.xml")
    if(key=="id") or (key=="lat"):
        xpath="/locations/location[@"+key+operand+value+"]"
    else:
        xpath="/locations/location["+key+operand+"\'"+value+"\']"
    rss=xml.xpathEval(xpath)
    metad=xml.xpathEval("/locations/metadata")
    print("Content-type: application/xml; charset=UTF-8\n")
    print("<locations>")
    print metad[0]
    for node in rss:
        print node
    print("</locations>")
    return

def main():
    fs = cgi.FieldStorage()
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    if(not chiave) and (not confronto) and (not valore):
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
                filtraGT(chiave,valore,True, False)
            elif(confronto=="LT"):
                filtraGT(chiave,valore,False,False)
            elif(confronto=="GE"):
                filtraGT(chiave,valore,True,True)
            elif(confronto=="LE"):
                filtraGT(chiave,valore,False,True)
            

main()

def errhttp(errno):
    return


def filtraCONTAINS(key,value,ncontains):
    return