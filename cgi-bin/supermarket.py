#!/usr/bin/python

import cgi
import error
import json
from pprint import  pprint
import copy
import operator

ops = {
"==": operator.eq,
"!=": operator.ne,
"<>": operator.ne,
"<": operator.lt,
"<=": operator.le,
">": operator.gt,
">": operator.ge
}

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
           key = key.encode('utf-8')
        if isinstance(value, unicode):
           value = value.encode('utf-8')
        elif isinstance(value, list):
           value = _decode_list(value)
        elif isinstance(value, dict):
           value = _decode_dict(value)
        rv[key] = value
    return rv


def filtraEQ(key,value,nequal):
        if(nequal):
                op="=="
        else:
                op="!="
        data=open("../data/supermarketBO2011.json", "r").read()
        orig=json.loads(data, object_hook=_decode_dict)
        jdata=copy.deepcopy(orig)
        print("Content-type: application/json; UTF-8\n")
        for item, subdict in orig.iteritems():
                for subkey,val in subdict.iteritems():
                        if ((key in val) and ops[op](val[key],value)):
                                del jdata["locations"][subkey]
        print json.dumps(jdata, sort_keys=True, indent=4)
    
def main():
    fs = cgi.FieldStorage()
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    if(not chiave) and (not confronto) and (not valore):
        xml=open("../data/supermarketBO2011.bin", "r")
        print("Content-type: application/json; charset=UTF-8\n")
        content=xml.read()
        print content
    else:
        if(not chiave) or (not confronto) or (not valore):
            error.errhttp("406")
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
