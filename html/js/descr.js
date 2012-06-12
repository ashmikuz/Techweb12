var descr = new Array();
descr["trovapernome"] = false;
descr["apertoind"] = false;
descr["vicinoa"] = false;

var arrayname = new Array();
arrayname[0] = "farmacie";
arrayname[1] = "supermarket";
arrayname[2] = "poste";
arrayname[3] = "medici";
arrayname[4] = "materne";

var Latitude, Longitude;
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

function getdescrurl(descrname, args) {
	var url = new Array();
	var urlcounter = 0;
	if(descrname == "vicinoa") {
		var lat = args["lat"];
		var longitude = args["long"];
		for(i=0; i< arrayname.length;i++) {
			if(document.getElementById(arrayname[i]).checked) {
				var path = "http://ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + arrayname[i] + "/params/" + lat + "/" + longitude + "/10";
				url[urlcounter] = path;
				urlcounter++;
			}
		}
	}
	/*if(descrname == "apertoind") {
		var giorno = args["giorno"];
		var longitude = args["long"];
		for(name in ["farmacie", "supermarker", "poste", "medici", "materne"]) {
			if(document.getElementById(name).checked) {
				url.push("ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + name + "/params/" + lat + "/" + longitude + "/10");
			}
		}
	}
	if(descrname == "trovapernome") {
		var lat = args["lat"];
		var longitude = args["long"];
		for(name in ["farmacie", "supermarker", "poste", "medici", "materne"]) {
			if(document.getElementById(name).checked) {
				url.push("ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + name + "/params/" + lat + "/" + longitude + "/10");
			}
		}
	}*/
	//console.log(url);
	return url;
}

function descrfilter(arg, descrname) {
	descr[descrname] = true;
	cancelladescr(descrname);
	//clean grid and map
	cleargrid();
	removemarkers(undefined);
	if( descrname = 'vicinoa') {
		var lat, lng;
		geocoder.geocode({
			'address' : arg + ",40100 Bologna",
			'region' : 'it'
		}, function(results, status) {
			if(status == google.maps.GeocoderStatus.OK) {
				/*recupero lat e long*/
				Latitude = results[0].geometry.location.lat();
				Longitude = results[0].geometry.location.lng();
				var ar = {"lat" : Latitude,	"long" : Longitude};
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
	//var url=getdescrurl(descrname, arg);
	
}