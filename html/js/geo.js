var mappa = null;
var markers = [];
var marker;

var icone = new Array()
icone['farmacia'] = "images/farmacia.png";
icone['medico di medicina generale'] = "images/medici.png";
icone['supermarket'] = "images/market.png";
icone['poste e telegrafi'] = "images/poste.png";
icone['scuola materna'] = "images/materne.png";
icone['farmacie'] = "images/farmacia.png";
icone['medici'] = "images/medici.png";
icone['supermarket'] = "images/market.png";
icone['poste'] = "images/poste.png";
icone['materne'] = "images/materne.png";

function errorgeo(error) {
	var pmaggiore = {};
	pmaggiore["coords"] = {};
	pmaggiore["coords"]["latitude"] = 44.4942;
	pmaggiore["coords"]["longitude"] = 11.3433;
	mostra_mappa(pmaggiore);
}

function inizialize() {
	if(navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(mostra_mappa, errorgeo);
	} else {
		var pmaggiore = {};
		pmaggiore["coords"] = {};
		pmaggiore["coords"]["latitude"] = 44.4942;
		pmaggiore["coords"]["longitude"] = 11.3433;
		mostra_mappa(pmaggiore);
		inizialize(pmaggiore);
	}
	/*se ricarico la pagina tutte le checkbox vengono "pulite" */
	var ins = document.getElementsByTagName('input');
	for(var i = 0; i < ins.length; i++) {
		if(ins[i].getAttribute('type') == 'checkbox') {
			ins[i].checked = false;
		}
	}
}

function mostra_mappa(posizione) {
	// identifico il punto in cui è stato individuato l'utente
	var punto = new google.maps.LatLng(posizione.coords.latitude, posizione.coords.longitude);
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

//function

function drawmarkers(checkbox) {
	xml = getxml(checkbox);
	var lat, longitude, id, marker, myLatlng, category, name, address, tel, opening, info;
	locations = xml.getElementsByTagName("location");
	//mappa=document.getElementById("mia_mappa");
	for( i = 0; i < locations.length; i++) {
		lat = locations[i].attributes.getNamedItem("lat").value;
		id = locations[i].attributes.getNamedItem("id").value;
		longitude = locations[i].attributes.getNamedItem("long").value;
		for( j = 0; j < locations[i].childNodes.length; j++) {
			if(locations[i].childNodes[j].tagName == "category") {
				if(window.ActiveXObject) {
					category = locations[i].childNodes[j].text.toLowerCase();
				} else {
					category = locations[i].childNodes[j].textContent.toLowerCase();
				}
			} else if(locations[i].childNodes[j].tagName == "name") {
				if(window.ActiveXObject) {
					name = locations[i].childNodes[j].text;
				} else {
					name = locations[i].childNodes[j].textContent;
				}

			} else if(locations[i].childNodes[j].tagName == "address") {
				if(window.ActiveXObject) {
					address = locations[i].childNodes[j].text;
				} else {
					address = locations[i].childNodes[j].textContent;
				}

			} else if(locations[i].childNodes[j].tagName == "tel") {
				if(window.ActiveXObject) {
					tel = locations[i].childNodes[j].text;
				} else {
					tel = locations[i].childNodes[j].textContent;
				}

			} else if(locations[i].childNodes[j].tagName == "opening") {
				if(window.ActiveXObject) {
					opening = locations[i].childNodes[j].text;
				} else {
					opening = locations[i].childNodes[j].textContent;
				}

			}
		}
		//document.getElementById("prova").innerHTML+= (id+","+lat+","+longitude+"<br/>");
		myLatlng = new google.maps.LatLng(parseFloat(lat), parseFloat(longitude));
		var icona = icone[category];
		contentString = generainfo(name, category, address, tel, opening);
		var infowindow = new google.maps.InfoWindow({
			content : contentString
		});
		marker = new google.maps.Marker({
			position : myLatlng,
			map : mappa,
			title : name,
			icon : icona,
			description : contentString
		});
		google.maps.event.addListener(marker, 'click', function() {
			infowindow.content = this.description;
			infowindow.open(mappa, this);
		});
		markers.push(marker);
	}
}

function removemarkers(category) {
	for( i = 0; i < markers.length; i++) {
		if(markers[i].getIcon() == icone[category]) {
			//alert("trovato!");
			markers[i].setMap(null);
			markers.splice(i, 1);
			i--;
		}
	}
}

function generainfo(name, category, address, tel, opening) {
	content = '<div><div id="loctitle">' + name + '</div>' + '<div id="category">' + category + '</div>' + '<div id="address">' + address + '</div>' + '<div id="tel">' + tel + '</div>' + '<div id="opening" >' + opening + '</div></div>';
	return content;
}