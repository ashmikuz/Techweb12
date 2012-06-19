var aggregatori = new Object();
aggregatori['farmacie'] = "http://ltw1218.web.cs.unibo.it/ltw1218-farmacie";
aggregatori['medici'] = "http://ltw1218.web.cs.unibo.it/ltw1218-medici";
aggregatori['supermarket'] = "http://ltw1218.web.cs.unibo.it/ltw1218-supermarket";
aggregatori['poste'] = "http://ltw1218.web.cs.unibo.it/ltw1218-poste";
aggregatori['materne'] = "http://ltw1218.web.cs.unibo.it/ltw1218-materne";

var aggrega = new Object();
aggrega['farmacia'] = "ltw1218-farmacie";
aggrega['medico di medicina generale'] = "ltw1218-medici";
aggrega['supermarket'] = "ltw1218-supermarket";
aggrega['poste e telegrafi'] = "ltw1218-poste";
aggrega['scuola materna'] = "ltw1218-materne";


var nodes;

function drawgrid(nodes)
{
	var xmlretval = loadXMLString("<locations></locations>");
	var xmlroot = xmlretval.getElementsByTagName("locations");
	var dataroot = data.getElementsByTagName("locations");
	var lunghezza = nodes.length;
	for(var j = 0; j < lunghezza; j++) {
		console.log(xmlroot[0]);
		console.log(nodes[j]);
		var clone=nodes[j].cloneNode(true)
		xmlroot[0].appendChild(clone);
		var el = nodes[j].cloneNode(true);
		dataroot[0].appendChild(el);
	}
	store.loadRawData(data);
	store.load();
	return xmlretval;
}

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


