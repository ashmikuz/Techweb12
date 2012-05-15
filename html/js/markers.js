
var aggregatori = new Array();
aggregatori['farmacie'] = "ltw1218-farmacie";
aggregatori['medici'] = "ltw1218-medici";
aggregatori['supermarket'] = "ltw1218-supermarket";
aggregatori['poste'] = "ltw1218-poste";
aggregatori['materne']= "ltw1218-materne"

function drawmarkers()
{
	xml=getxml()
}

function getxml()
{
	var xmlretval=new XpathResult();
	var xmlDoc=document.implementation.createDocument("","",null);
	xmlDoc.async=false;
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
					urlaggr="http://ltw1218.web.cs.unibo.it/ltw1218-"+checkboxes[i].id;					
					aggrxml=xmlDoc.load(urlaggr)
					document.evaluate("/locations/location", aggrxml,null ,XPathResult.ANY_TYPE, xmlretval);
				}
				
		}
	return retval;
	
}
