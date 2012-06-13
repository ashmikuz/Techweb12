Ext.require(['Ext.data.*', 'Ext.grid.*']);

var categorie = new Array();
categorie['farmacie'] = "farmacia";
categorie['medici'] = "Medico di Medicina Generale";
categorie['supermarket'] = "supermarket";
categorie['poste'] = "Poste e Telegrafi";
categorie['materne'] = "Scuola Materna";

var aggrega = new Object();
aggrega['farmacia'] = "ltw1218-farmacie";
aggrega['medico di medicina generale'] = "ltw1218-medici";
aggrega['supermarket'] = "ltw1218-supermarket";
aggrega['poste e telegrafi'] = "ltw1218-poste";
aggrega['scuola materna'] = "ltw1218-materne";


var store;
var grid;
var categlist;
var data;
data = newDocument("locations", ""); data

//Definisco la feature per raggruppare le location per categoria
var groupingFeature = Ext.create('Ext.grid.feature.Grouping', {
	groupHeaderTpl : '{name}'
});

function removegrid(checkboxid) {
	categlist = data.getElementsByTagName("category");
	max = categlist.length;
	for( i = 0; i < max; i++) {
		if(categlist[i].textContent == categorie[checkboxid]) {
			data.getElementsByTagName("locations")[0].removeChild(categlist[i].parentNode);
			max--;
			i--;
		}
	}
	store.loadRawData(data);
	store.load();
}

function cleargrid() {
	loclist = data.getElementsByTagName("location");
	var i = 0;
	while(data.getElementsByTagName("location").length > 0) {
		data.getElementsByTagName("locations")[0].removeChild(loclist[0]);
	}
	store.loadRawData(data);
	store.load();
}

Ext.onReady(function() {

	Ext.define('Location', {
		extend : 'Ext.data.Model',
		fields : [
		// set up the fields mapping into the xml doc
		'category', 'name', 'address', 'tel', {
			name : 'lat',
			mapping : '@lat'
		}, {
			name : 'long',
			mapping : '@long'
		}, {
			name : 'id',
			mapping : '@id'
		}, 'opening', 'closing']
	});

	// create the Data Store
	store = Ext.create('Ext.data.Store', {
		model : 'Location',
		autoLoad : true,
		autoSync : true,
		autoShow : true,
		groupField : 'category',
		data : data,
		proxy : {
			type : 'memory',
			// the return will be XML, so lets set up a reader
			reader : {
				type : 'xml',
				// records will have an "Item" tag
				record : 'location',
			},
		}
	});

	// create the grid
	grid = Ext.create('Ext.grid.Panel', {
		store : store,
		features : [groupingFeature],

		columns : [{
			text : "Nome",
			width : 190,
			dataIndex : 'name',
			sortable : true
		}, {
			text : "Indirizzo",
			width : 210,
			dataIndex : 'address',
			sortable : true
		}, {
			text : "Telefono",
			width : 115,
			dataIndex : 'tel',
			sortable : true
		}, {
			text : "Apertura",
			flex : 1,
			dataIndex : 'opening',
			sortable : true
		}],
		renderTo : 'tabella',
		layout : 'fit'
	});

	// update panel body on selection change
	grid.getSelectionModel().on('selectionchange', function(sm, selectedRecord) {
		if(selectedRecord.length) {
			Ext.create('Ext.window.Window', {
				title : selectedRecord[0].data["name"] + ' - ' + selectedRecord[0].data["category"],
				height : 400,
				width : 400,
				layout : 'fit',
				html : generainfo(selectedRecord[0].data["id"] , aggrega[selectedRecord[0].data["category"].toLowerCase()]),
			}).show();
		}

	});
});
