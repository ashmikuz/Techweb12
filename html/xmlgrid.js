Ext.require([
    'Ext.data.*',
    'Ext.grid.*'
]);

Ext.onReady(function(){
    Ext.define('Farmacie',{
        extend: 'Ext.data.Model',
        fields: [
            // set up the fields mapping into the xml doc
            // The first needs mapping, the others are very basic
            //{name: 'name', mapping: 'location > name'},
            'name', 'address', 'tel'
        ]
    });

    // create the Data Store
    var store = Ext.create('Ext.data.Store', {
        model: 'Farmacie',
        autoLoad: true,
        proxy: {
            // load using HTTP
            type: 'ajax',
            url: '../data/farmacieBO2011.xml',
            // the return will be XML, so lets set up a reader
            reader: {
                type: 'xml',
                // records will have an "Item" tag
                record: '/locations/location',
                idProperty: '@id',
                totalRecords: '@total'
            }
        }
    });

    // create the grid
    var grid = Ext.create('Ext.grid.Panel', {
        store: store,
        columns: [
            {text: "Nome", flex: 1, dataIndex: 'name', sortable: true},
            {text: "Indirizzo", width: 180, dataIndex: 'address', sortable: true},
            {text: "Telefono", width: 115, dataIndex: 'tel', sortable: true}
        ],
        renderTo:'example-grid',
        width: 540,
        height: 200
    });
});