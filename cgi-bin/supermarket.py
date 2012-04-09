#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import os
import error
import json
import codecs
import copy
import operator
from costanti import supermarket, uencoding, mimejson


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
        print("Content-type: application/json; charset=UTF-8\n")
        for item, subdict in orig.iteritems():               
                for subkey,val in subdict.iteritems():
                        if((key == "lat,long") and ("lat" in val) and ("long" in val) and (ops[op](val["lat"].encode(uencoding),lat) and (ops[op](val["long"].encode(uencoding),long)))):
                           del jdata["locations"][subkey]
                        elif((key=="category") and ("category" in val)):
                            for i in range(0, len(val["category"])):
                                if(ops[op](val["category"][i].lower().encode(uencoding), value)):
                                    del jdata["locations"][subkey]
                        elif((key=="id") and (item!="metadata") and ops[op](subkey.lower().encode(uencoding), value)):
                            del jdata["locations"][subkey]
                        elif ((key in val) and ops[op]((val[key].lower().encode(uencoding)),value)):
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
    print("Content-type: application/json; charset=UTF-8\n")
    for item, subdict in orig.iteritems():
        for subkey,val in subdict.iteritems():
            if((key=="category") and ("category" in val)):
                for i in range(0, len(val["category"])):
                    if(ops[op](value in val["category"][i].lower().encode(uencoding))):
                        del jdata["locations"][subkey]
            elif((key=="id") and (item!="metadata") and ops[op](value in subkey.lower().encode(uencoding))):
                del jdata["locations"][subkey]
            elif ((key in val) and ops[op](value in (val[key].lower()))):
                del jdata["locations"][subkey]
    print json.dumps(jdata, ensure_ascii=False, encoding=uencoding ,sort_keys=True, indent=4).encode(uencoding)
    
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
    lat,long=value.split(",")
    data=open(supermarket, "r").read()
    orig=json.loads(data)
    jdata=copy.deepcopy(orig)
    print("Content-type: application/json; charset=UTF-8\n")
    for item, subdict in orig.iteritems():
        for subkey,val in subdict.iteritems():
            if(("lat" in val) and ("long" in val) and (ops[op](float(lat), float(val["lat"])) and (ops[op](float(long), float(val["long"]))))):
                del jdata["locations"][subkey]
    print json.dumps(jdata, ensure_ascii=False, encoding=uencoding ,sort_keys=True, indent=4).encode(uencoding)     
    
def main():
    fs = cgi.FieldStorage()
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    """
    questa parte serve per controllare che json in questo caso sia accettato dal descrittore. tuttavia se la abilitiamo adesso, siccome il browser non accetta json non va...
    la lascio commentata finche non iniziamo con i descrittori
    if(error.testenviron(os.environ, mimejson)):
        return
    """
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
