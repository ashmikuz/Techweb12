#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import os
import codecs
import string
import urllib
import error
import sys
sys.path.append("/home/web/ltw1131/cgi-bin/libs/")
from lxml import etree
from costanti import uencoding, farmacie

maiusstr=u"ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÒÙ"
minusstr=u"abcdefghijklmnopqrstuvwxyzàèéòù"


def filtraEQ(key, value, nequal):
    if(nequal):
        operand="!="
    else:
        operand="="
    xml=etree.parse(farmacie)
    query=""
    if(key=="id"):
        query="/locations/location[translate(@"+key+",\'abcdefghijklmnopqrstuvwxyz1234567890\',\'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\')"+operand+"\'"+value+"\']"
    if (key=="lat,long"):
        lat,long=value.split(",")
        query="/locations/location[@lat"+operand+"\'"+lat+"\'and @long"+operand+"\'"+long+"\' ]"
    if(key=="name") or (key=="category"):
        rss=xml.xpath("/locations/location[translate("+key+',"'+maiusstr+'", "'+minusstr+'")'+operand+'"'+value+'"]')
    if(query==""):
        error.errhttp("406")
        return
    print("Content-type: text/plain; charset=UTF-8\n")
    print (repr(query))
    rss=xml.xpath("/locations/location[translate("+key+',"'+maiusstr+'", "'+minusstr+'")'+operand+'"'+value+'"]')
    metad=xml.xpath("/locations/metadata")
    output=etree.Element("locations")
    for element in metad:
        output.append(element)
    for node in rss:
        output.append(node)
    print(etree.tostring(output, pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE locations SYSTEM "http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DTDs/locations.dtd">',  encoding=uencoding))
    return
    
def filtraGT(key,value,greaterthan, equal):
    if(greaterthan):
        operand=">"
    else:
        operand="<"
    if(equal):
        operand+="="
    xml=libxml2.parseFile(farmacie)
    if(key=="lat,long"):
        lat,long=value.split(",")
        xpath="/locations/location[@lat"+operand+"\'"+lat+"\'and @long"+operand+"\'"+long+"\' ]"
        rss=xml.xpathEval(xpath)
        metad=xml.xpathEval("/locations/metadata")
        print("Content-type: application/xml; charset=UTF-8\n")
        print("<locations>")
        print metad[0]
        for i in range(node.size()):
            print node
        print("</locations>")
    else:
        error.errhttp("406")
    return

def filtraCONTAINS(key,value,ncontains):
    if(ncontains):
        operator="not (contains"
    else:
        operator="(contains"
    xpath=""
    if((key=="id") and (not ncontains)):
        xpath="/locations/location[contains(@id,\'"+value+"\')]"
    if((key=="name") or (key=="category") or (key=="opening") or (key=="closing")):
        xpath="/locations/location["+operator+"("+key+",\'"+value+"\'))]"
    if((key=="address") and (not ncontains)):
        xpath="/locations/location[contains(address,\'"+value+"\')]"
    if(xpath==""):
        error.errhttp("406")
        return
    xml=libxml2.parseFile(farmacie)
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
        xml=open(farmacie, "r")
        print("Content-type: application/xml; charset=UTF-8\n")
        content=xml.read()
        print content
    else:
        if(not chiave) or (not confronto) or (not valore):
            error.errhttp("406")
        else:
            chiave=chiave.lower().decode(encoding)
            confronto=confronto.lower().decode(encoding)
            valore=valore.lower().decode(encoding)
            if(confronto=="eq"):
                filtraEQ(chiave, valore, False)
            elif(confronto=="neq"):
                filtraEQ(chiave,valore,True)
            elif(confronto=="contains"):
                filtraCONTAINS(chiave,valore, False)
            elif(confronto=="ncontains"):
                filtraCONTAINS(chiave,valore,True)
            elif(confronto=="gt"):
                filtraGT(chiave,valore,True, False)
            elif(confronto=="lt"):
                filtraGT(chiave,valore,False,False)
            elif(confronto=="ge"):
                filtraGT(chiave,valore,True,True)
            elif(confronto=="le"):
                filtraGT(chiave,valore,False,True)
            else:
                error.errhttp("406")
            

main()
