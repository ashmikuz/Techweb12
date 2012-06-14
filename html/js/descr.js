var descr = {"trovapernome": false, "apertoind":false, "vicinoa":false};

var descrarg;

var arrayname = new Array();
arrayname[0] = "farmacie";
arrayname[1] = "supermarket";
arrayname[2] = "poste";
arrayname[3] = "medici";
arrayname[4] = "materne";

var Latitude, Longitude;
var vicinoamarker;
var geocoder = new google.maps.Geocoder();

function cancelladescr(descrname) {
	if(descrname != "trovapernome") {
		descr["trovapernome"] = false;
	}
	if(descrname != "apertoind") {
		descr["apertoind"] = false;
	}
	if(descrname != "vicinoa") {
		descr["vicinoa"] = false;
	}
}


function getdescrurl(descrname, args, aggr) {
			var url = new Array();
			var urlcounter = 0;
			var path;
			descrarg=args;
			console.log(descrname);
			if(descrname == "vicinoa") {
				var lat = args["lat"];
				var longitude = args["lng"];
				if(!aggr)
				{
					for(i=0; i< arrayname.length;i++) 
					{
						if(document.getElementById(arrayname[i]).checked) 
						{
							path = "http://ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + arrayname[i] + "/params/" + lat + "/" + longitude + "/10";
							url[urlcounter] = path;
							urlcounter++;
						}
					}
				}
				else
					{
						path = "http://ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + aggr + "/params/" + lat + "/" + longitude + "/10"
						url[0]=path;
						urlcounter=1;
					}
			}
	if(descrname == "apertoind") {
		if(!aggr)
		{
				for(var i=0; i< arrayname.length;i++) 
				{
					if(document.getElementById(arrayname[i]).checked) 
					{
				path="apertoind/ltw1218-" + arrayname[i] + "/params/AND/"+args;
				url[urlcounter]=path;
				urlcounter++;
			}
		}
		}
		else
			{
			path="apertoind/ltw1218-" + aggr + "/params/AND/"+args;
			url[0]=path;
			urlcounter=1;
			}
	}
	if(descrname == "trovapernome") {
		var name=args;
		if(!aggr)
		{
				for(var i=0; i< arrayname.length;i++) 
				{
					if(document.getElementById(arrayname[i]).checked) 
					{
				path="trova-per-nome/ltw1218-" + arrayname[i] + "/params/"+args;
				url[urlcounter]=path;
				urlcounter++;
			}
		}
		}
		else
			{
			path="trova-per-nome/ltw1218-" + aggr + "/params/"+args;
			url[0]=path;
			urlcounter=1;
			}
	}
	//console.log(url);
	return url;
}

function descrfilter(arg, descrname) {
	descr[descrname] = true;
	cancelladescr(descrname);
	//clean grid and map
	cleargrid();
	removemarkers(undefined);
	console.log(descrname);
	if( descrname == 'vicinoa') {
		var lat, lng;
		if(typeof(arg)=="string")
		{
		geocoder.geocode({
			'address' : arg + ",40100 Bologna",
			'region' : 'it'
		}, function(results, status) {
			if(status == google.maps.GeocoderStatus.OK) {
				/*recupero lat e long*/
				Latitude = results[0].geometry.location.lat();
				Longitude = results[0].geometry.location.lng();
				var ar = {"lat" : Latitude,	"lng" : Longitude};
				createposmarker(ar);
				var patharray = getdescrurl(descrname, ar);
				for(var i=0;i<patharray.length;i++){
					//alert(patharray[i]);
					var xml = loadXMLDoc(patharray[i]);
					var xmlroot = xml.getElementsByTagName("location");
					drawgrid(xmlroot);
					drawmarkers(xmlroot);
				}
			} else {
				alert("Indirizzo non trovato: " + status);
			}
		});
		}
		else
			{
			var patharray = getdescrurl(descrname, arg);
			for(var i=0;i<patharray.length;i++){
				//alert(patharray[i]);
				var xml = loadXMLDoc(patharray[i]);
				var xmlroot = xml.getElementsByTagName("location");
				drawgrid(xmlroot);
				drawmarkers(xmlroot);
			}
			}
	}
	else
		{
			var patharray = getdescrurl(descrname, arg);
			for(var i=0;i<patharray.length;i++){
				//alert(patharray[i]);
				var xml = loadXMLDoc(patharray[i]);
				var xmlroot = xml.getElementsByTagName("location");
				drawgrid(xmlroot);
				drawmarkers(xmlroot);
			}
		}
	//var url=getdescrurl(descrname, arg);
	
}

function createposmarker(pos)
{
	var markerlatlng= new google.maps.LatLng(pos["lat"], pos["lng"]);
	vicinoamarker = new google.maps.Marker({
		position : markerlatlng,
		map : mappa,
		icon: icone["vicinoa"],
		title : "Posizione ricerca"
	});
	mappa.setCenter(markerlatlng);
}

function miapos()
{
	descrfilter({"lat": punto.lat(),"lng": punto.lng()}, "vicinoa");
}