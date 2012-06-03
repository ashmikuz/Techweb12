#!/usr/bin/python
# -*- coding: utf-8 -

import os
import codecs
import error
from costanti import uencoding, mimecsv, smaterne, medici, mimexml
import cgi
import csv
import operator
import sys

ops = {
  "==": operator.eq,
  "!=": operator.ne,
  "<": operator.lt,
  "<=": operator.le,
  ">": operator.gt,
  ">=": operator.ge,
  "not": operator.not_,
  "id": operator.truth
  }


dial=csv.Dialect
dial.quoting=csv.QUOTE_ALL
dial.quotechar='"'
dial.delimiter=","
dial.lineterminator="\n"
dial.escapechar="\\"

def filtraEQ(key,value,nequal, dsource):
    if(nequal):
        op="!="
    else:
        op="=="
    if(key != "id" and key != "name" and key != "lat" and key!="long" and key != "category"):
        error.errcode("406")
        return
    key=key[0].upper()+key[1:]
    data=open(dsource,"r")
    orig=csv.DictReader(data)
    result=csv.DictWriter(sys.stdout, orig.fieldnames, dialect=dial)
    print("Content-type: text/csv; charset=UTF-8\n")
    result.writeheader()
    for item in orig:
        if(ops[op](item[key].lower(), value)):
            result.writerow(item)
            
            
def filtraCONTAINS(key,value,ncontains, dsource):
    if(ncontains):
        op="not"
    else:
        op="id"
    if(key != "id" and key != "name" and key != "category" and key != "address" and key != "opening" and key != "closing"):
        error.errcode("406")
        return
    if(ncontains and key == "address"):
        error.errcode("406")
        return
    key=key[0].upper()+key[1:]
    data=open(dsource,"r")
    orig=csv.DictReader(data)
    result=csv.DictWriter(sys.stdout, orig.fieldnames, dialect=dial)
    print("Content-type: text/csv; charset=UTF-8\n")
    result.writeheader()
    for item in orig:
        if(ops[op](value in item[key].lower())):
            result.writerow(item)    
    
def filtraGT(key,value,greaterthan, equal, dsource):
    if(greaterthan):
        op=">"
    else:
        op="<"
    if(not equal):
        op+="="
    if(key!="lat" and key!="long"):
        error.errcode("406")
        return
    data=open(dsource,"r")
    orig=csv.DictReader(data)
    key=key[0].upper()+key[1:]
    result=csv.DictWriter(sys.stdout, orig.fieldnames, dialect=dial)
    print("Content-type: text/csv; charset=UTF-8\n")
    result.writeheader()
    for item in orig:
      if(ops[op](float(item[key]), float(value))):
          result.writerow(item)
      

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr")
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    if(aggr=="materne"):
        source=smaterne
    elif(aggr=="medici"):
        source=medici
    else:
        error.errhttp("404")
    if(not chiave) and (not confronto) and (not valore) and not error.testenviron(os.environ, mimexml):
        xml=os.path.splitext(source)[0]+".xml"
        file=open(xml, "r")
        print("Content-type: application/xml; charset=UTF-8\n")
        content=file.read()
        print content
        return
    """
    questa parte serve per controllare che json in questo caso sia accettato dal descrittore. tuttavia se la abilitiamo adesso, siccome il browser non accetta json non va...
    la lascio commentata finche non iniziamo con i descrittori"""
    if(error.testenviron(os.environ, mimecsv)):
        error.errhttp("406")
        return
    if(not chiave) and (not confronto) and (not valore):
        file=open(source, "r")
        print("Content-type: text/csv; charset=UTF-8\n")
        content=file.read()
        print content
    else:
        if(not chiave) or (not confronto) or (not valore):
            error.errhttp("406")
        else:
            chiave=chiave.lower().decode(uencoding)
            confronto=confronto.lower().decode(uencoding)
            valore=valore.lower().decode(uencoding)
            if(confronto=="eq"):
                filtraEQ(chiave, valore, False, source)
            elif(confronto=="neq"):
                filtraEQ(chiave,valore,True, source)
            elif(confronto=="contains"):
                filtraCONTAINS(chiave,valore, False, source)
            elif(confronto=="ncontains"):
                filtraCONTAINS(chiave,valore,True, source)
            elif(confronto=="gt"):
                filtraGT(chiave,valore,True, False, source)
            elif(confronto=="lt"):
                filtraGT(chiave,valore,False,False,source)
            elif(confronto=="ge"):
                filtraGT(chiave,valore,True,True, source)
            elif(confronto=="le"):
                filtraGT(chiave,valore,False,True, source)
            else:
                error.errcode("406")
                
            

main()
