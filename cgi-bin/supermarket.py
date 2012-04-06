#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import os
import error
import json
import codecs
from pprint import  pprint
import copy
import operator
from costanti import supermarket, uencoding

ops = {
"==": operator.eq,
"!=": operator.ne,
"<>": operator.ne,
"<": operator.lt,
"<=": operator.le,
">": operator.gt,
">": operator.ge,
"not": operator.not_,
"id": operator.truth
}

def filtraEQ(key,value,nequal):
        if(nequal):
                op="=="
        else:
                op="!="
        if(key != "id" and key != "name" and key != "lat,long" and key != "category"):
            error.errcode("406")
            return
        data=open(supermarket, "r").read()
        if(key=="lat,long"):
            lat,long=value.split(",")
        orig=json.loads(data)
        jdata=copy.deepcopy(orig)
        print("Content-type: application/json; UTF-8\n")
        for item, subdict in orig.iteritems():
                for subkey,val in subdict.iteritems():
                        if((key == "lat,long") and ("lat" in val) and ("long" in val) and (ops[op](val["lat"],lat) and (ops[op](val["ong"],long)))):
                           del jdata["locations"][subkey]
                        if ((key in val) and ops[op]((val[key].lower().decode(uencoding)),value)):
                            del jdata["locations"][subkey]
        print json.dumps(jdata, ensure_ascii=False, encoding=uencoding, sort_keys=True, indent=4).encode(uencoding)
        
def filtraCONTAINS(key,value,ncontains):
    if(ncontains):
        op="id"
    else:
        op="not"
    if(key != "id" and key != "name" and key != "category" and key != "address" and key != "opening" and key != "closing"):
        error.errcode("406")
        return
    if(ncontains and key == "address"):
        error.errcode("406")
        return
    data=open(supermarket, "r").read()
    orig=json.loads(data)
    jdata=copy.deepcopy(orig)
    print("Content-type: application/json; UTF-8\n")
    for item, subdict in orig.iteritems():
        for subkey,val in subdict.iteritems():
            if ((key in val) and ops[op](value in (val[key].lower().decode(uencoding)))):
                del jdata["locations"][subkey]
    print json.dumps(jdata, ensure_ascii=False, sort_keys=True, indent=4).encode(uencoding)
        
    
def main():
    fs = cgi.FieldStorage()
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    if(not chiave) and (not confronto) and (not valore):
        xml=open(supermarket, "r")
        print("Content-type: application/json; charset=UTF-8\n")
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
            elif(confronto=="contains"):
                filtraCONTAINS(chiave,valore,True)
            elif(confronto=="gt"):
                filtraGT(chiave,valore,True, False)
            elif(confronto=="lt"):
                filtraGT(chiave,valore,False,False)
            elif(confronto=="ge"):
                filtraGT(chiave,valore,True,True)
            elif(confronto=="le"):
                filtraGT(chiave,valore,False,True)
            

main()
