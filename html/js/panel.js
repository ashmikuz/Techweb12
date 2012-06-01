	var altezza = 600;
	var lunghezza =1000;
	var targetRender = 'container';
	
	
		var aggr = Ext.create('Ext.Panel', {
		title: 'Aggregatori',
		html: '&lt;Sex Pisto&gt;',
		cls:'empty'
	});

	var descr1 = Ext.create('Ext.Panel', {
		title: 'Vicino a',
		html: '&lt;Sex Pisto&gt;',
		cls:'empty'
	});

	var descr2 = Ext.create('Ext.Panel', {
		title: 'Aperto in data',
		html: '&lt;Sex Pisto&gt;',
		cls:'empty'
	});
		
	// Panel for the west
    var accordionPanel = new Ext.Panel({
	    // xtype: 'panel' implied by default
	    region:'west',
	    xtype: 'panel',
	    margins: '5 0 0 5',
	    width: 200,
	    collapsible: true,   // make collapsible
	    id: 'west-region-container',
	    layout:'accordion',
        items: [aggr, descr1, descr2]
    });

	var MainTab = new Ext.TabPanel({
        layout: 'fit',
        activeTab: 0,
        layoutOnTabChange : true,
        defaults :{
            bodyPadding: 0
        },
        items: [{
            html: '<div id="mia_mappa"><center>Caricamento in corso...</center>',
            title: 'Mappa'
        },{
            items:[grid], 
            title: 'Tabella'
        }]
	});
	
	var mainPanel = new Ext.Panel({
	    region: 'center',     // center region is required, no width/height specified
	    xtype: 'panel',
	    layout: 'fit',
	    items: [MainTab],
		margins: '5 5 0 0'
    });
	
Ext.onReady(function() {

/*Creo il pannello generale che contiene tutto*/
	Ext.create('Ext.panel.Panel', {
	    width: lunghezza,
	    height: altezza,
	    layout:'border',
	    items: [accordionPanel,mainPanel],
	    renderTo: targetRender
	});
});