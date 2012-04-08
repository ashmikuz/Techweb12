#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import os
import codecs
import string
import urllib
import error
import sys
sys.path.append("/home/web/ltw1218/cgi-bin/libs/")
from lxml import etree
from costanti import uencoding, farmacie, maiusstr, minusstr


def filtraEQ(key, value, nequal):
    if(nequal):
        operand="!="
    else:
        operand="="
    xml=etree.parse(farmacie)
    if(key=="id"):
        rss=xml.xpath("/locations/location[translate(@"+key+",\'"+maiusstr+"\',\'"+minusstr+"\')"+operand+"\'"+value+"\']")
    elif (key=="lat,long"):
        lat,long=value.split(",")
        rss=xml.xpath("/locations/location[translate(@lat"+operand+"\'"+lat+"\'and @long"+operand+"\'"+long+"\' ]")
    elif(key=="name") or (key=="category"):
        rss=xml.xpath("/locations/location[translate("+key+',"'+maiusstr+'", "'+minusstr+'")'+operand+'"'+value+'"]')
    else:
        error.errhttp("406")
        return
    print("Content-type: application/xml; charset=UTF-8\n")
    metad=xml.xpath("/locations/metadata")
    output=etree.Element("locations")
    for met in metad:
        output.append(met)
    for loc in rss:
        output.append(loc)
    print(etree.tostring(output, pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE locations SYSTEM "http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DTDs/locations.dtd">',  encoding=uencoding))
    return
    
def filtraGT(key,value,greaterthan, equal):
    if(greaterthan):
        operand=">"
    else:
        operand="<"
    if(equal):
        operand+="="
    xml=etree.parse(farmacie)
    if(key=="lat,long"):
        lat,long=value.split(",")
        rss=xml.xpath("/locations/location[@lat"+operand+"\'"+lat+"\'and @long"+operand+"\'"+long+"\' ]")
        metad=xml.xpath("/locations/metadata")
        output=etree.Element("locations")
        for met in metad:
            output.append(met)
        for loc in rss:
            output.append(loc)
        print("Content-type: application/xml; charset=UTF-8\n")
        print(etree.tostring(output, pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE locations SYSTEM "http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DTDs/locations.dtd">',  encoding=uencoding))
    else:
        error.errhttp("406")
    return

def filtraCONTAINS(key,value,ncontains):
    if(ncontains):
        operator="not (contains"
    else:
        operator="(contains"
    xml=etree.parse(farmacie)
    if((key=="id") and (not ncontains)):
        rss=xml.xpath("/locations/location[contains(translate(@id,'"+maiusstr+"','"+minusstr+"'), '"+value+"')]")
    elif((key=="name") or (key=="category") or (key=="opening") or (key=="closing")):
        rss=xml.xpath("/locations/location["+operator+"(translate("+key+",'"+maiusstr+"','"+minusstr+"'),'"+value+"'))]")
    elif((key=="address") and (not ncontains)):
        rss=xml.xpath("/locations/location[contains(translate(address,'"+maiusstr+"','"+minusstr+"'),'"+value+"')]")
    else:
        error.errhttp("406")
        return
    metad=xml.xpath("/locations/metadata")
    output=etree.Element("locations")
    print("Content-type: application/xml; charset=UTF-8\n")
    for met in metad:
        output.append(met)
    for loc in rss:
        output.append(loc)
    print(etree.tostring(output, pretty_print=True, xml_declaration=True, doctype='<!DOCTYPE locations SYSTEM "http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DTDs/locations.dtd">',  encoding=uencoding))   
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
            chiave=chiave.lower().decode(uencoding)
            confronto=confronto.lower().decode(uencoding)
            valore=valore.lower().decode(uencoding)
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
