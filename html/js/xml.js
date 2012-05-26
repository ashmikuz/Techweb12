var aggregatori = new Array();
aggregatori['farmacie'] = "http://ltw1218.web.cs.unibo.it/ltw1218-farmacie";
aggregatori['medici'] = "http://ltw1218.web.cs.unibo.it/converti/ltw1218-medici";
aggregatori['supermarket'] = "http://ltw1218.web.cs.unibo.it/converti/ltw1218-supermarket";
aggregatori['poste'] = "http://ltw1218.web.cs.unibo.it/converti/ltw1218-poste";
aggregatori['materne']= "http://ltw1218.web.cs.unibo.it/converti/ltw1218-materne";
var nodes;

function getxml(checkbox)
		{
			var xmlretval=newDocument("locations","");
			var xmlroot=xmlretval.getElementsByTagName("locations");
			var aggrxml;
			var el;
			var checkboxes=new Array();
			//checkboxes[0]=document.getElementById("farmacie");
			//checkboxes[1]=document.getElementById("materne");
			//checkboxes[2]=document.getElementById("poste");
			//checkboxes[3]=document.getElementById("supermarket");
			//checkboxes[4]=document.getElementById("medici");
			if (checkbox.checked)
			{
				urlaggr=aggregatori[checkbox.id];					
				nodes=loadXMLDoc(urlaggr).getElementsByTagName("location");
				dataroot=data.getElementsByTagName("locations")
				var lunghezza=nodes.length;
				for (j=0; j<lunghezza;j++)
					{
						xmlroot[0].appendChild(nodes[j].cloneNode(true));
						el=nodes[j].cloneNode(true);
						dataroot[0].appendChild(el);
					}
				store.loadRawData(data);
				store.load();
			}
			else
				{
					removemarkers(checkbox.id);
					removegrid(checkbox.id);
				}
			return xmlretval;
		}

function loadXMLDoc(dname)
{
if (window.XMLHttpRequest)
  {
  xhttp=new XMLHttpRequest();
  }
else
  {
  xhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xhttp.open("GET",dname,false);
xhttp.setRequestHeader("Content-type","application/xml");
xhttp.send();
return xhttp.responseXML;
}

function loadXMLString(txt) 
{
if (window.DOMParser)
  {
  parser=new DOMParser();
  xmlDoc=parser.parseFromString(txt,"text/xml");
  }
else // Internet Explorer
  {
  xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
  xmlDoc.async=false;
  xmlDoc.loadXML(txt); 
  }
return xmlDoc;
}

newDocument = function(rootTagName, namespaceURL) {
    if (!rootTagName) rootTagName = "";
    if (!namespaceURL) namespaceURL = "";

    if (document.implementation && document.implementation.createDocument) {
        // This is the W3C standard way to do it
        return document.implementation.createDocument(namespaceURL, 
                       rootTagName, null);
    }
    else { // This is the IE way to do it
        // Create an empty document as an ActiveX object
        // If there is no root element, this is all we have to do
        var doc = new ActiveXObject("MSXML2.DOMDocument");

        // If there is a root tag, initialize the document
        if (rootTagName) {
            // Look for a namespace prefix 
            var prefix = "";
            var tagname = rootTagName;
            var p = rootTagName.indexOf(':');
            if (p != -1) {
                prefix = rootTagName.substring(0, p);
                tagname = rootTagName.substring(p+1);
            }

            // If we have a namespace, we must have a namespace prefix
            // If we don't have a namespace, we discard any prefix
            if (namespaceURL) { 
                if (!prefix) prefix = "a0"; // What Firefox uses
            }
            else prefix = "";

            // Create the root element (with optional namespace) as a
            // string of text
            var text = "<" + (prefix?(prefix+":"):"") + tagname +
                (namespaceURL
                 ?(" xmlns:" + prefix + '="' + namespaceURL +'"')
                 :"") +
                "/>";
            // And parse that text into the empty document
            doc.loadXML(text);
        }
        return doc;
    }
};
