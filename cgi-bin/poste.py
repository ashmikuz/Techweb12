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
    result.bind('', rdflib.URIRef('http://www.essepuntato.it/resource/', False))
    result.bind('vcard', rdflib.URIRef('http://www.w3.org/2006/vcard/ns#'))
    result.bind('cs', rdflib.URIRef('http://cs.unibo.it/ontology/'))
    result.bind('dcterms', rdflib.URIRef('http://purl.org/dc/terms/'))
    result.bind('xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))
    result.bind('this', rdflib.URIRef('http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl'))
    if nequal:
        nop="!"
    else:
        oquery="""
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX cs: <http://cs.unibo.it/ontology/>
        PREFIX : <http://www.essepuntato.it/resource/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX this: <http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl>
        CONSTRUCT {?s ?p ?o}
        WHERE {
                ?s ?p ?o.
                ?s dcterms:creator "Working Group LTW 2011/2012"
                }
        """
        query_meta=src.query(oquery)
        for element in query_meta:
            result.add(element)
        nop=""
    if(key=="id"):
        squery="""
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX cs: <http://cs.unibo.it/ontology/>
        PREFIX : <http://www.essepuntato.it/resource/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX this: <http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl>
        CONSTRUCT {?s ?p ?o}
        WHERE {
                ?s ?p ?o.
                FILTER ("""+nop+"""regex (?s ,"^http://www.essepuntato.it/resource/"""+value+"""$", "i"))
                }
        """
    else:
        squery="""
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX cs: <http://cs.unibo.it/ontology/>
        PREFIX : <http://www.essepuntato.it/resource/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX this: <http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/DataSource2/posteBO2011.ttl>
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