#!/usr/bin/python
# -*- coding: utf-8 -

import os
import codecs
import error
from costanti import uencoding, mimecsv, smaterne
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

file

dial=csv.Dialect
dial.quoting=csv.QUOTE_ALL
dial.quotechar='"'
dial.delimiter=","
dial.lineterminator="\n"
dial.escapechar="\\"

def filtraEQ(key,value,nequal):
    if(nequal):
        op="!="
    else:
        op="=="
    if(key != "id" and key != "name" and key != "lat,long" and key != "category"):
        error.errcode("406")
        return
    if(key=="lat,long"):
        lat,longi=value.split(",")
    else:
        key=key[0].upper()+key[1:]
    data=open(file,"r")
    orig=csv.DictReader(data)
    result=csv.DictWriter(sys.stdout, orig.fieldnames, dialect=dial)
    print("Content-type: text/csv; charset=UTF-8\n")
    result.writeheader()
    for item in orig:
        if(key!=u"lat,long"):
            if(ops[op](item[key].lower(), value)):
                result.writerow(item)
        elif(ops[op](item["Lat"], lat) and (ops[op](item["Long"], longi))):
            result.writerow(item)
            
            
def filtraCONTAINS(key,value,ncontains):
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
    data=open(file,"r")
    orig=csv.DictReader(data)
    result=csv.DictWriter(sys.stdout, orig.fieldnames, dialect=dial)
    print("Content-type: text/csv; charset=UTF-8\n")
    result.writeheader()
    for item in orig:
        if(ops[op](value in item[key].lower())):
            result.writerow(item)    
    
def filtraGT(key,value,greaterthan, equal):
    if(greaterthan):
        op=">"
    else:
        op="<"
    if(not equal):
        op+="="
    if(key!="lat,long"):
        error.errcode("406")
        return
    lat,longi=value.split(",")
    data=open(file,"r")
    orig=csv.DictReader(data)
    result=csv.DictWriter(sys.stdout, orig.fieldnames, dialect=dial)
    print("Content-type: text/csv; charset=UTF-8\n")
    result.writeheader()
    for item in orig:
      if(ops[op](float(item["Lat"]), float(lat)) and (ops[op](float(item["Long"]), float(longi)))):
          result.writerow(item)
      

def main():
    fs = cgi.FieldStorage()
    aggr=fs.getvalue("aggr")
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    if(aggr=="materne"):
        file=materne
    if(aggr=="medici"):
        file=medici
    else:
        error.errhttp("404")
    """
    questa parte serve per controllare che json in questo caso sia accettato dal descrittore. tuttavia se la abilitiamo adesso, siccome il browser non accetta json non va...
    la lascio commentata finche non iniziamo con i descrittori
    if(error.testenviron(os.environ, mimecsv)):
        return
    """
    if(not chiave) and (not confronto) and (not valore):
        file=open(file, "r")
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
                error.errcode("406")
                
            

main()
