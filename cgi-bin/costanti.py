#!/usr/bin/python
# -*- coding: utf-8 -*-

uencoding="utf-8"
farmacie="../data/farmacieBO2011.xml"
supermarket="../data/supermarketBO2011.json"
smaterne="../data/scuolematerneBO2011.csv"
poste="../data/posteBO2011.ttl"
medici="../data/mediciDiFamiglia2012.csv"
maiusstr=u"ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÒÙ"
minusstr=u"abcdefghijklmnopqrstuvwxyzàèéòù"
mimexml="application/xml"
mimejson="application/json"
mimecsv="text/csv"
mimeturtle="tex/turtle"
vcurl="http://www.w3.org/2006/vcard/ns#"
dcturl="http://purl.org/dc/terms/"
fourl="http://xmlns.com/foaf/spec/index.rdf"
csvfields="\"Id\",\"Category\",\"Name\",\"Address\",\"Lat\",\"Long\",\"subcategory\",\"note\",\"Opening\",\"Closing\",\"Creator\",\"Created\",\"Valid\",\"Version\",\"Source\""
metacat="http://vitali.web.cs.unibo.it/twiki/pub/TechWeb12/MetaCatalogo1112/metaCatalogo.xml"
weekdays=["mon","tue","wed","thu","fri","sat","sun"]
months=["jan","feb","mar","apr","may","jun","jul","aug","sept","oct","nov","dec"]