	var altezza = 550;
	var lunghezza =1000;
	var targetRender = 'container';
	
Ext.onReady(function() {
	//pannello che contiene i controlli per caricare da aggregatori
		var aggr = Ext.create('Ext.Panel', {
		title: 'Categorie',
		contentEl:'box1',
		//html: '&lt;Sex Pisto&gt;',
		cls:'empty'
	});
	//vicino a
	var descr1 = Ext.create('Ext.Panel', {
		title: 'Vicino a',
		contentEl:'box2',
		cls:'empty'
	});
	//aperto in data
	var descr2 = Ext.create('Ext.Panel', {
		title: 'Aperto in data',
		contentEl:'box3',
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
            bodyPadding: 0,
            autoScroll:true
        },
        items: [{
        	contentEl:'mia_mappa',
            title: 'Mappa'
        },{
            items:[grid], 
            title: 'Tabella'
        },{
        	contentEl:'info',
            title: 'Help'
        }]
	});
	
	var mainPanel = new Ext.Panel({
	    region: 'center',     // center region is required, no width/height specified
	    xtype: 'panel',
	    layout: 'fit',
	    items: [MainTab],
		margins: '5 5 0 0'
    });
	

/*Creo il viewport generale che contiene tutto*/
	Ext.create('Ext.Viewport', {
	    layout:'anchor',
	    listeners:
	    	{
	    	resize: {
	    		fn: function()
	    		{
	    			punto=mappa.getCenter();
	    			google.maps.event.trigger(mappa, "resize");
	    			mappa.setCenter(punto);
	    		}
	    	}
	    	},
	    items: [
	            {
	            	xtype:'panel',
	            	layout:'fit',
	            	border: false,
	            	anchor: '100%',
	            	height: 70,
	            	minHeight: 70,
	            	html: '<div style="color:white ;font-size:500%; text-align:center;">MAL</div>',
	            	bodyStyle:{"background-color":"#333333"}
	            },
	            {
	            	xtype:'panel',
	            	layout:'border',
	            	border:false,
	            	items: [accordionPanel,mainPanel],
	            	anchor: '80%, -80',
	            	style: {
	            	        marginLeft: 'auto',
	            	        marginRight: 'auto'
	            	}
	            }
	]
	    //renderTo: targetRender
	});
});