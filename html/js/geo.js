var mappa;
		function errorgeo(error)
		{
			var pmaggiore={};
			pmaggiore["coords"]={};
			pmaggiore["coords"]["latitude"]=44.4942;
			pmaggiore["coords"]["longitude"]=11.3433;
			mostra_mappa(pmaggiore);
		}
		
		function inizialize() 
		{
  			navigator.geolocation.getCurrentPosition(mostra_mappa, errorgeo);
		}
		
		function mostra_mappa(posizione) 
		{
	 		// identifico il punto in cui è stato individuato l'utente
  			var punto = new google.maps.LatLng(posizione.coords.latitude, posizione.coords.longitude),
  			// definisco una serie di opzioni          
  			opzioni = 
  			{
    			zoom: 15,
    			center: punto,
    			mapTypeId: google.maps.MapTypeId.ROADMAP
  			},
  			// definisco l'elemento della pagina che ospiterà la mappa
  			contenitore = document.getElementById("mia_mappa"),
  			// creo la mappa
  			mappa = new google.maps.Map(contenitore, opzioni),
  			// imposto un marker
  			marker = new google.maps.Marker(
  				{
    				position: punto,
    				map: mappa,
    				title: "Tu sei qui!"
  				});
		}
