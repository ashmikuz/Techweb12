/*variabile usata per tenere in memoria quale è il descrittore usato:
 * si presuppone che se tutti siano false allora stiamo caricando da aggregatore
 */
var descr = {
	"trovapernome" : false,
	"apertoind" : false,
	"vicinoa" : false
};

var arrayname = new Array();
arrayname[0] = "farmacie";
arrayname[1] = "supermarket";
arrayname[2] = "poste";
arrayname[3] = "medici";
arrayname[4] = "materne";

var Latitude, Longitude;
var vicinoamarker;
var geocoder = new google.maps.Geocoder();

/*fa in modo che descrname sia l'unico descrittore attivo*/
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

/*
 * Argomenti: descrname: , args: specifica gli argomenti(ad esempio lat long), aggr: specifica l'aggregatore,
 * Return: i/gli url per le interrogazioni server side
 */
function getdescrurl(descrname, args, aggr) {
	var url = new Array();
	var urlcounter = 0;
	var path;
	descrarg = args;
	/*vicino a*/
	if(descrname == "vicinoa") {
		var lat = args["lat"];
		var longitude = args["lng"];
		/*se l'aggregatore non è definito*/
		if(!aggr) {
			/*ciclo su tutte le categorie e vefirico se le checkbox sono checked*/
			for( i = 0; i < arrayname.length; i++) {
				if(document.getElementById(arrayname[i]).checked) {
					path = "http://ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + arrayname[i] + "/params/" + lat + "/" + longitude + "/10";
					url[urlcounter] = path;
					urlcounter++;
				}
			}
		} else {/*se l'aggregatore è definito*/
			path = "http://ltw1218.web.cs.unibo.it/vicinoa/ltw1218-" + aggr + "/params/" + lat + "/" + longitude + "/10"
			url[0] = path;
			urlcounter = 1;
		}
	}
	/*aperto in data*/
	if(descrname == "apertoind") {
		/*se l'aggregatore non è definito ciclo su tutti e verifico se sono selezionati*/
		if(!aggr) {
			for(var i = 0; i < arrayname.length; i++) {
				if(document.getElementById(arrayname[i]).checked) {
					path = "apertoind/ltw1218-" + arrayname[i] + "/params/AND/" + args;
					url[urlcounter] = path;
					urlcounter++;
				}
			}
		} else {
			path = "apertoind/ltw1218-" + aggr + "/params/AND/" + args;
			url[0] = path;
			urlcounter = 1;
		}
	}
	/*trova per nome*/
	if(descrname == "trovapernome") {
		var name = args;
		/*se l'aggregatore non è definito ciclo su tutti e verifico se sono selezionati*/
		if(!aggr) {
			for(var i = 0; i < arrayname.length; i++) {
				if(document.getElementById(arrayname[i]).checked) {
					path = "trova-per-nome/ltw1218-" + arrayname[i] + "/params/" + args;
					url[urlcounter] = path;
					urlcounter++;
				}
			}
		} else {
			path = "trova-per-nome/ltw1218-" + aggr + "/params/" + args;
			url[0] = path;
			urlcounter = 1;
		}
	}
	return url;
}

/*funzione richiamata dai pulsanti dei descrittori, nel caso di vicinoa fa qualche operazione aggiuntiva senno
 * controlla se sono selezionati dei descrittori e poi invoca la getdescrurl
 */
function descrfilter(arg, descrname) {
	descr[descrname] = true;
	//cancello gli altri descrittori da quelli selezionati
	cancelladescr(descrname);
	//clean grid and map
	cleargrid();
	removemarkers(undefined);
	if(arg == "") {
		alert("Inserisci un indirizzo o utilizza la tua posizione!");
		return;
	}
	if(descrname == 'vicinoa') {
		var lat, lng;
		if( typeof (arg) == "string") {
			geocoder.geocode({
				'address' : arg + ",40100 Bologna",
				'region' : 'it'
			}, function(results, status) {
				if(status == google.maps.GeocoderStatus.OK) {
					/*recupero lat e long*/
					Latitude = results[0].geometry.location.lat();
					Longitude = results[0].geometry.location.lng();
					var ar = {
						"lat" : Latitude,
						"lng" : Longitude
					};
					/*crea il marker posizione sulla mappa*/
					createposmarker(ar);
					var patharray = getdescrurl(descrname, ar);
					if(patharray.length == 0) {
						alert("Seleziona almeno una categoria!");
						return;
					}
					for(var i = 0; i < patharray.length; i++) {
						var xml = loadXMLDoc(patharray[i]);
						var xmlroot = xml.getElementsByTagName("location");
						drawgrid(xmlroot);
						drawmarkers(xmlroot);
					}
				} else {
					alert("Indirizzo non trovato: " + status);
					return;
				}
			});
		} else {
			var patharray = getdescrurl(descrname, arg);
			if(patharray.length == 0) {
				alert("Seleziona almeno una categoria!");
				return;
			}
			for(var i = 0; i < patharray.length; i++) {
				//alert(patharray[i]);
				var xml = loadXMLDoc(patharray[i]);
				var xmlroot = xml.getElementsByTagName("location");
				drawgrid(xmlroot);
				drawmarkers(xmlroot);
			}
		}
	} else {
		descrarg = arg;
		var patharray = getdescrurl(descrname, arg);
		if(patharray.length == 0) {
			alert("Seleziona almeno una categoria!");
			return;
		}
		for(var i = 0; i < patharray.length; i++) {
			//alert(patharray[i]);
			var xml = loadXMLDoc(patharray[i]);
			var xmlroot = xml.getElementsByTagName("location");
			drawgrid(xmlroot);
			drawmarkers(xmlroot);
		}
	}
	//var url=getdescrurl(descrname, arg);

}

/*funzione che quando si utilizza il descrittore vicinoa crea un marker alla posizione specificata
 * dall'utente
 */
function createposmarker(pos) {
	var markerlatlng = new google.maps.LatLng(pos["lat"], pos["lng"]);
	vicinoamarker = new google.maps.Marker({
		position : markerlatlng,
		map : mappa,
		icon : icone["vicinoa"],
		title : "Posizione ricerca"
	});
	mappa.setCenter(markerlatlng);
}

/*funzione per utilizzare il descrittore aperto
 * si costruiscono i parametri e dopo si invia la richiesta al server, in caso di errore
 * si ritorna la stringa vuota
 */
function getaperto(multiint) {
	var date = new Date();
	var day = date.getDate().toString();
	var month = ("0" + (date.getMonth() + 1)).slice(-2);
	var year = date.getFullYear().toString();
	var hour = ("0" + date.getHours()).slice(-2);
	var startminute = ("0" + date.getMinutes()).slice(-2);
	var endminute = ("0" + (date.getMinutes() + 10)).slice(-2);
	var formatteddate = year + "-" + month + "-" + day + ": " + hour + startminute + "-" + hour + endminute + ".";
	var urldescr = "aperto/params/" + multiint + "/" + formatteddate;
	var client = new XMLHttpRequest();
	client.open('GET', urldescr, false);
	client.send();
	if(client.responseText == 1) {
		return '<div style="color:#00FF00">Aperto</div>';
	}
	if(client.responseText == 0) {
		return '<div style="color:#FF0000">Chiuso</div>';
	} else {
		return "";
	}
}

/*invoca descrfilter passando automaticamente come parametro la posizione rilevata dell'utente e selezionando
 * il descrittore vicinoa
 */
function miapos() {
	mappa.setCenter(punto);
	descrfilter({
		"lat" : punto.lat(),
		"lng" : punto.lng()
	}, "vicinoa");
}