var mappa = null;
var markers = [];
var punto;
var descrarg;

/*associo a una categoria l'immagine relativa*/
var icone = new Object();
icone['farmacia'] = "images/farmacia.png";
icone['medico di medicina generale'] = "images/medici.png";
icone['supermarket'] = "images/market.png";
icone['poste e telegrafi'] = "images/poste.png";
icone['scuola materna'] = "images/materne.png";
icone['vicinoa'] = "images/zoom.png";

function errorgeo(error) {
	var pmaggiore = {};
	pmaggiore["coords"] = {};
	pmaggiore["coords"]["latitude"] = 44.4942;
	pmaggiore["coords"]["longitude"] = 11.3433;
	mostra_mappa(pmaggiore);
}

/*funzione invocata onload: richiede la geolocalizzazione e in caso negativo imposta un punto predefinito,
 * e resetto tutte le checkbox
 */
function inizialize() {
	if(navigator.geolocation) {
		var location_timeout = setTimeout("errorgeo()", 3000);
		navigator.geolocation.getCurrentPosition(mostra_mappa, errorgeo);
	} else {
		var pmaggiore = {};
		pmaggiore["coords"] = {};
		pmaggiore["coords"]["latitude"] = 44.4942;
		pmaggiore["coords"]["longitude"] = 11.3433;
		mostra_mappa(pmaggiore);
	}
	/*se ricarico la pagina tutte le checkbox vengono "pulite" */
	var ins = document.getElementsByTagName('input');
	for(var i = 0; i < ins.length; i++) {
		if(ins[i].getAttribute('type') == 'checkbox') {
			ins[i].checked = false;
		}
	}
}

/*creo la mappa e geolocalizzo il punto in cui si trova l'utente*/
function mostra_mappa(posizione) {
	// identifico il punto in cui è stato individuato l'utente
	punto = new google.maps.LatLng(posizione.coords.latitude, posizione.coords.longitude);
	// definisco una serie di opzioni
	var opzioni = {
		zoom : 15,
		center : punto,
		mapTypeId : google.maps.MapTypeId.ROADMAP
	};
	// definisco l'elemento della pagina che ospiterà la mappa
	var contenitore = document.getElementById("mia_mappa");
	// creo la mappa
	mappa = new google.maps.Map(contenitore, opzioni);
	// imposto un marker
	var mypos = new google.maps.Marker({
		position : punto,
		map : mappa,
		title : "Tu sei qui!"
	});
}

function activeaggr(checkbox) {
	var i;
	for(i in descr) {
		if(descr[i]) {
			var urldescr = getdescrurl(i, descrarg, checkbox);
			var xml = loadXMLDoc(urldescr).getElementsByTagName("location");
			drawmarkers(xml);
			drawgrid(xml);
			return true;
		}
	}
	return false;
}

function drawaggr(checkbox) {
	if(checkbox.checked) {
		if(activeaggr(checkbox.id) == true) {
			return;
		}
		var xml = getxml(checkbox);
		drawmarkers(xml);
		drawgrid(xml);
	} else {
		removemarkers(checkbox.id);
		removegrid(checkbox.id);
	}
}

function crossbrowsertext(node)
{
	if(window.ActiveXObject) {
		return node.text.toLowerCase();
	} else {
		return node.textContent.toLowerCase();
	}
}

function drawmarkers(locations) {
	var lat, longitude, id, myLatlng, category, name, address, tel, opening, info;
	for( i = 0; i < locations.length; i++) {
		lat = locations[i].attributes.getNamedItem("lat").value;
		id = locations[i].attributes.getNamedItem("id").value;
		longitude = locations[i].attributes.getNamedItem("long").value;
		opening = "";
		for( j = 0; j < locations[i].childNodes.length; j++) {
			if(locations[i].childNodes[j].tagName == "category") {
				category=crossbrowsertext(locations[i].childNodes[j]);
			} else if(locations[i].childNodes[j].tagName == "name") {
				name=crossbrowsertext(locations[i].childNodes[j]);
			} else if(locations[i].childNodes[j].tagName == "address") {
				address=crossbrowsertext(locations[i].childNodes[j]);

			} else if(locations[i].childNodes[j].tagName == "tel") {
				tel=crossbrowsertext(locations[i].childNodes[j]);

			} else if(locations[i].childNodes[j].tagName == "opening") {
				opening+=crossbrowsertext(locations[i].childNodes[j]);
			}
		}
		myLatlng = new google.maps.LatLng(parseFloat(lat), parseFloat(longitude));
		var icona = icone[category];
		//contentString = generainfo(name, category, address, tel, opening);
		//contentString = generainfo(id, aggrega[category]);
		var infowindow = new google.maps.InfoWindow({
			//content : contentString
		});
		marker = new google.maps.Marker({
			position : myLatlng,
			map : mappa,
			id : id,
			title : name,
			opening : opening,
			categoria : category,
			icon : icona,
			//description : contentString
		});
		google.maps.event.addListener(marker, 'click', function() {
			infowindow.content = generainfo(this.id, aggrega[category]) + getaperto(this.opening);
			infowindow.open(mappa, this);
		});
		markers.push(marker);
	}
}

function removemarkers(category) {
	if(vicinoamarker) {
		vicinoamarker.setMap(null);
	}
	for(var i = 0; i < markers.length; i++) {
		if(category == undefined || markers[i].categoria == categorie[category].toLowerCase()) {
			markers[i].setMap(null);
			markers.splice(i, 1);
			i--;
		}
	}
}

/*function generainfo(name, category, address, tel, opening) {
 content = '<div><div id="loctitle">' + name + '</div>' + '<div id="category">' + category + '</div>' + '<div id="address">' + address + '</div>' + '<div id="tel">' + tel + '</div>' + '<div id="opening" >' + opening + '</div></div>';
 return content;
 }*/