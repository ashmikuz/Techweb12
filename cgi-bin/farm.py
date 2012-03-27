#!/usr/bin/python

import cgi
import os
import string


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
    return

def filtraCONTAINS(key,value,ncontains):
    return