#!/usr/bin/python
# -*- coding: utf-8 -

import sys
import cgi
import error
from costanti import mimeturtle, poste, uencoding, fourl, vcurl, dcturl
sys.path.append("/home/web/ltw1218/cgi-bin/libs/")
import rdflib
from rdflib import plugin
import rdfextras

vcard=rdflib.Namespace(vcurl)
dcterms=rdflib.Namespace(dcturl)
foaf=rdflib.Namespace(fourl)

campi = {
u"name": u"vcard:fn",
u"id" : u"vcard:category",
u"lat" : u"vcard:latitude",
u"long" : u"vcard:longitude",
u"address" : u"vcard:extended-address",
u"category" : u"vcard:category",
u"opening" : u"cs:opening",
u"closing" : u"cs:closing"
}

plugin.register('sparql', rdflib.query.Processor, 'rdfextras.sparql.processor', 'Processor')
plugin.register('sparql', rdflib.query.Result, 'rdfextras.sparql.query', 'SPARQLQueryResult')


def filtraEQ(key,value,nequal):
    turtle=rdflib.Graph()
    src=turtle.parse(poste, format='n3')
    result=rdflib.Graph()
    if nequal:
        nop="!"
    else:
        nop=""
    if(key=="id"):
        squery="""
        CONSTRUCT {?s ?p ?o}
        WHERE {
                ?s ?p ?o.
                FILTER ("""+nop+"""regex (?s ,"^http://www.essepuntato.it/resource/"""+value+"""$", "i"))
                }
        """
    else:
        squery="""
        CONSTRUCT {?s ?p ?o}
        WHERE {
                ?s ?p ?o;
                """+campi[key]+""" ?name.
                FILTER ("""+nop+"""regex (?name ,"^"""+value+"""$", "i"))
                }
        """
    print("Content-type: text/turtle; charset=UTF-8\n")
    query_result=src.query(squery)
    print squery
    for element in query_result:
        result.add(element)
    print result.serialize(format="n3")

def main():
    fs = cgi.FieldStorage()
    chiave=fs.getvalue("key")
    confronto=fs.getvalue("comp")
    valore=fs.getvalue("value")
    """
    questa parte serve per controllare che json in questo caso sia accettato dal descrittore. tuttavia se la abilitiamo adesso, siccome il browser non accetta json non va...
    la lascio commentata finche non iniziamo con i descrittori
    if(error.testenviron(os.environ, mimeturtle)):
        return
    """
    if(not chiave) and (not confronto) and (not valore):
        file=open(poste, "r")
        print("Content-type: text/turtle; charset=UTF-8\n")
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