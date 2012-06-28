/*Array di indirizzi degli aggregatori*/
var aggregatori = new Object();
aggregatori['farmacie'] = "http://ltw1218.web.cs.unibo.it/ltw1218-farmacie";
aggregatori['medici'] = "http://ltw1218.web.cs.unibo.it/ltw1218-medici";
aggregatori['supermarket'] = "http://ltw1218.web.cs.unibo.it/ltw1218-supermarket";
aggregatori['poste'] = "http://ltw1218.web.cs.unibo.it/ltw1218-poste";
aggregatori['materne'] = "http://ltw1218.web.cs.unibo.it/ltw1218-materne";

/*Array dei nomi degli aggregatori*/
var aggrega = new Object();
aggrega['farmacia'] = "ltw1218-farmacie";
aggrega['medico di medicina generale'] = "ltw1218-medici";
aggrega['supermarket'] = "ltw1218-supermarket";
aggrega['poste e telegrafi'] = "ltw1218-poste";
aggrega['scuola materna'] = "ltw1218-materne";

/* Aggiungo i nodi passati per argomento alla griglia (aggiungendoli alla variabile data), la ridisegno
 * e ritorno i nodi aggiunti
 */
function drawgrid(nodes)
{
	var xmlretval = loadXMLString("<locations></locations>");
	var xmlroot = xmlretval.getElementsByTagName("locations");//variabile per aggiungere i nodi a xmlretval
	var dataroot = data.getElementsByTagName("locations");//variabile per aggiungere i nodi a data
	var lunghezza = nodes.length;
	for(var j = 0; j < lunghezza; j++) {
		/*console.log("xmlroot[0]");
		console.log(xmlroot[0]);
		console.log("nodes["+j+"]");
		console.log(nodes[j]);*/
		var clone=nodes[j].cloneNode(true)
		xmlroot[0].appendChild(clone);
		var el = nodes[j].cloneNode(true);
		dataroot[0].appendChild(el);
	}
	store.loadRawData(data);
	store.load();
	console.log("xmlretval");
	console.log(xmlretval);
	return xmlretval;
}

/*Crea un xml passandole la checkbox dell'aggregatore
 * se la checkbox è checked allora invoca loadXMLDoc e restituisce i nodi
 * altrimenti restituisce un insieme vuoto di nodi location
 */
function getxml(checkbox) {
	var aggrxml;
	var el;
	var xmlretval;
	if(checkbox.checked) {
		urlaggr = aggregatori[checkbox.id];
		xmlretval = loadXMLDoc(urlaggr);
	} else {
		xmlretval = newDocument("locations", "");
		removemarkers(checkbox.id);
		removegrid(checkbox.id);
	}
	return (xmlretval.getElementsByTagName("location"));
}

/*carica un xml da Path*/
function loadXMLDoc(dname) {
	if(window.XMLHttpRequest) {
		xhttp = new XMLHttpRequest();
	} else {
		xhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xhttp.open("GET", dname, false);
	xhttp.setRequestHeader("Content-type", "application/xml");
	xhttp.send();
	return xhttp.responseXML;
}

/*converte il testo txt in un file xml*/
function loadXMLString(txt) {
	if(window.DOMParser) {
		parser = new DOMParser();
		xmlDoc = parser.parseFromString(txt, "text/xml");
	} else// Internet Explorer
	{
		xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		xmlDoc.async = false;
		xmlDoc.loadXML(txt);
	}
	return xmlDoc;
}

/*funzione per creare un nuovo documento*/
newDocument = function(rootTagName, namespaceURL) {
	if(!rootTagName)
		rootTagName = "";
	if(!namespaceURL)
		namespaceURL = "";
	if(document.implementation && document.implementation.createDocument) {
		// This is the W3C standard way to do it
		return document.implementation.createDocument(namespaceURL, rootTagName, null);
	} else {// This is the IE way to do it
		// Create an empty document as an ActiveX object
		// If there is no root element, this is all we have to do
		var doc = new ActiveXObject("MSXML2.DOMDocument");
		// If there is a root tag, initialize the document
		if(rootTagName) {
			// Look for a namespace prefix
			var prefix = "";
			var tagname = rootTagName;
			var p = rootTagName.indexOf(':');
			if(p != -1) {
				prefix = rootTagName.substring(0, p);
				tagname = rootTagName.substring(p + 1);
			}
			// If we have a namespace, we must have a namespace prefix
			// If we don't have a namespace, we discard any prefix
			if(namespaceURL) {
				if(!prefix)
					prefix = "a0";
				// What Firefox uses
			} else
				prefix = "";
			// Create the root element (with optional namespace) as a
			// string of text
			var text = "<" + ( prefix ? (prefix + ":") : "") + tagname + ( namespaceURL ? (" xmlns:" + prefix + '="' + namespaceURL + '"') : "") + "/>";
			// And parse that text into the empty document
			doc.loadXML(text);
		}
		return doc;
	}
};

/*funzione che dato un id e il nome di un aggregatore restituisce il lavoro del descrittore descrizione*/
function generainfo(id, aggr) {
	var Url = "http://ltw1218.web.cs.unibo.it/descrizione/" + aggr + "/params/" + id;
	if(window.XMLHttpRequest) {
		xhttp = new XMLHttpRequest();
	} else {
		xhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xhttp.open("GET", Url, false);
	xhttp.send();
	return xhttp.responseText;
}
