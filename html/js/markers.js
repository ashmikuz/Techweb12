
var aggregatori = new Array();
aggregatori['farmacie'] = "http://ltw1218.web.cs.unibo.it/ltw1218-farmacie";
aggregatori['medici'] = "http://ltw1218.web.cs.unibo.it/converti/ltw1218-medici";
aggregatori['supermarket'] = "http://ltw1218.web.cs.unibo.it/converti/ltw1218-supermarket";
aggregatori['poste'] = "http://ltw1218.web.cs.unibo.it/converti/ltw1218-poste";
aggregatori['materne']= "http://ltw1218.web.cs.unibo.it/converti/ltw1218-materne";

var markers = [];

function drawmarkers(checkbox)
{
	xml=getxml(checkbox);
	var lat,longitude,id,marker,myLatlng,map;
	locations=xml.getElementsByTagName("location");
	//mappa=document.getElementById("mia_mappa");
	for (i=0; i<locations.length; i++)
		{
			lat=locations[i].attributes.getNamedItem("lat").value;
			id=locations[i].attributes.getNamedItem("id").value;
			longitude=locations[i].attributes.getNamedItem("long").value;
			//document.getElementById("prova").innerHTML+= (id+","+lat+","+longitude+"<br/>");
			myLatlng = new google.maps.LatLng(parseFloat(lat),parseFloat(longitude));
			marker = new google.maps.Marker({
	            position: myLatlng,
	            map: mappa,
	            title:id
	        });			
			markers.push(marker);
		}
}

/*function getxml()
{
	var xmlretval=newDocument("locations","");
	var xmlroot=xmlretval.getElementsByTagName("locations");
	var aggrxml;
	var checkboxes=new Array();
	checkboxes[0]=document.getElementById("farmacie");
	checkboxes[1]=document.getElementById("materne");
	checkboxes[2]=document.getElementById("poste");
	checkboxes[3]=document.getElementById("supermarket");
	checkboxes[4]=document.getElementById("medici");
	for (i=0; i<5; i++)
		{
			if(checkboxes[i].checked)
				{
					urlaggr=aggregatori[checkboxes[i].id];					
					aggrxml=loadXMLDoc(urlaggr);
					nodes=aggrxml.getElementsByTagName("location");
					for (j=0; j<nodes.length;j++)
						{
							xmlroot[0].appendChild(nodes[j]);
						}
				}
				
		}
	return xmlretval;
	
}*/

