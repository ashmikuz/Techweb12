Ext.require([
    'Ext.data.*',
    'Ext.grid.*'
]);

var data;
var store;
var grid;
data=newDocument("locations","");

    //Definisco la feature per raggruppare le location per categoria
	var groupingFeature = Ext.create('Ext.grid.feature.Grouping',{
	    groupHeaderTpl: '{name}'
	});

function changesource()
{
	data=loadXMLDoc("converti/ltw1218-supermarket");
	store.loadRawData(data);
}

Ext.onReady(function(){
    Ext.define('Location',{
        extend: 'Ext.data.Model',
        fields: [
            // set up the fields mapping into the xml doc
          	'category',
            'name',
          	'address',
            'tel',
          	{name: 'lat', mapping: '@lat'},
          	{name: 'long', mapping: '@long'},
          	{name: 'id', mapping: '@id'},
          	'opening',
          	'closing'
        ]
    });

    // create the Data Store
    store = Ext.create('Ext.data.Store', {
        model: 'Location',
        autoLoad: true,
        autoSync: true,
        autoShow: true,
        groupField: 'category',
        data: data,
        proxy : {
        	type: 'memory',
            // the return will be XML, so lets set up a reader
            reader: {
                type: 'xml',
                // records will have an "Item" tag
                record: 'location',
            },
        }
    });
   

    // create the grid
    grid = Ext.create('Ext.grid.Panel', {
        store: store,
        features: [groupingFeature],
        columns: [
            {text: "Nome", flex: 1, dataIndex: 'name', sortable: true},
            {text: "Indirizzo", width: 180, dataIndex: 'address', sortable: true},
            {text: "Telefono", width: 115, dataIndex: 'tel', sortable: true}
        ],
        renderTo:'tabella',
        layout:'fit'
    });

});
