	var altezza = 550;
	var lunghezza =1000;
	var targetRender = 'container';
	var accordionh;
	
Ext.onReady(function() {
	//pannello che contiene i controlli per caricare da aggregatori
		var aggr = Ext.create('Ext.Panel', {
		title: 'Categorie',
		layout: 'fit',
		//flex:1,
		border: false,
		xtype: 'panel',
		contentEl:'box1',
		//html: '&lt;Sex Pisto&gt;',
		//cls:'empty'
	});
	//vicino a
	var descr1 = Ext.create('Ext.Panel', {
		title: 'Vicino a',
		layout: 'fit',
		contentEl:'box2',
		cls:'empty'
	});
	//aperto in data
	var descr2 = Ext.create('Ext.Panel', {
		title: 'Aperto in data',
		layouyt: 'fit',
		contentEl:'box3',
		cls:'empty'
	});
	
	var descr3 = Ext.create('Ext.Panel', {
		title: 'Trova',
		layouyt: 'fit',
		contentEl:'box4',
		cls:'empty'
	});
	
	
	accordionh=((Ext.getBody().getViewSize().height) - 225);
	
	// Panel for the west
    var accordionPanel = new Ext.Panel({
	    // xtype: 'panel' implied by default
	    //collapsible: true,   // make collapsible
	    id: 'west-region-container',
	    layout:'accordion',
	    height: accordionh,
	    minHeight: 145,
	    items: [descr1, descr2, descr3]
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
	    border: false,
    });
	
	var leftPanel = new Ext.Panel({
	    //region: 'west',
	    layout: {
	        type: 'vbox',
	        align : 'stretch',
	        pack  : 'start'
	    },
	    items: [
	           aggr
	           ,
	        	accordionPanel
	            ],
    });
	

/*Creo il viewport generale che contiene tutto*/
	var viewport=Ext.create('Ext.Viewport', {
	    layout:'anchor',
	    autoScroll:true,
	    minHeight: 460,
	    minWidth: 750,
	    listeners:
	    	{
	    	resize: {
	    		fn: function()
	    		{
	    			if(mappa!=null)
	    			{
	    			punto=mappa.getCenter();
	    			google.maps.event.trigger(mappa, "resize");
	    			mappa.setCenter(punto);
	    			}
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
	            	html: '<div style="color:black ;font-size:500%; text-align:center;">MAL</div>',
	            	bodyStyle:"background-image:url(images/texture.jpg) !important; background-repeat: repeat;"
	            },
	            {
	            	xtype:'panel',
	            	layout:'border',
	            	border:false,
	            	minHeight: 380,
	            	minWidth: 600,
	            	items: [{
	            			xtype: 'panel',
	            			region: 'west',
	            	    	collapsible: true,
	            	    	minHeight: 300,
	            	    	minWidth: 150,
	            	        items:[leftPanel]
	            			},mainPanel],
	            	anchor: '80%, -80',
	            	style: {
	            			split: true,
	            	        marginLeft: 'auto',
	            	        marginRight: 'auto'
	            	}
	            }
	]
	    //renderTo: targetRender
	});
	
	Ext.EventManager.onWindowResize(function () {
		accordionh=((Ext.getBody().getViewSize().height) - 225);
		accordionPanel.setHeight(accordionh);
    });
});