
	var accordionh;
	
Ext.onReady(function() {
	//pannello che contiene i controlli per caricare da aggregatori
		var aggr = Ext.create('Ext.Panel', {
		title: '<img src="images/categoria.png" width="18px" height="18px" alt="categorie" /> &nbsp Categorie',
		layout: 'fit',
		border: false,
		xtype: 'panel',
		contentEl:'box1',
		//cls:'empty'
	});
	//vicino a
	var descr1 = Ext.create('Ext.Panel', {
		title: '<img src="images/vicino.png" width="18px" height="18px" alt="categorie" />&nbsp<b>Vicino a:</b>',
		border: false,
		layout: 'fit',
		contentEl:'box2',
		cls:'empty',
		
	});
	
	
	//aperto in data
	var descr2 = Ext.create('Ext.Panel', {
		title: '<img src="images/aperto.png" width="18px" height="18px" alt="categorie" />&nbsp<b>Aperto in data:</b>',
		border: false,
		layouyt: 'fit',
		cls:'empty',
		//contentEl: 'datepicker',
		items:[
		       {
		    	   xtype:'panel',
		    	   border: false,
		    	   html:'<p style="text-align:center; padding-top: 5px;">Seleziona Data:</p>'
		       },
		       
		       {
		    	   xtype: 'datefield',
		           width: 140,
		           name: 'data',
		           format: 'Y-m-d',
		           listeners: {
		        	   select: {
		        	   fn :function(dp, date){
		        		   descrfilter(Ext.Date.format(date, 'Y-m-d').toString(), "apertoind");
		           }}},
		           style:
		        	   {
		        	   		marginTop: '5px',
		        			marginLeft: 'auto',
		        			marginRight: 'auto'
		        	   }
		           //maxValue: new Date()
		       }
		       ]
	});
	
	var descr3 = Ext.create('Ext.Panel', {
		title: '<img src="images/trova.png" width="18px" height="18px" alt="categorie" />&nbsp<b>Trova:</b>',
		border: false,
		labelStyle: 'font-weight:bold;',
		layouyt: 'fit',
		contentEl:'box4',
		cls:'empty',
		
	});
	
	
	accordionh=((Ext.getBody().getViewSize().height) - 243);
	
	// Panel for the west
    var accordionPanel = new Ext.Panel({
	    // xtype: 'panel' implied by default
	    //collapsible: true,   // make collapsible
	    id: 'west-region-container',
	    layout:'accordion',
	    height: accordionh,
	   	minHeight: 220,
	    width: 180,
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
            title: 'Mappa',
            bodyStyle:"background-image:url(images/texture.jpg); background-repeat: repeat;"
        },{
            items:[grid], 
            title: 'Tabella',
            bodyStyle:"background-image:url(images/texture.jpg); background-repeat: repeat;"
        },{
        	loader:
        		{
        			url: 'help.html',
        			contentType: 'html',
        			loadMask: false
        		},
        		listeners:
        			{
        			activate: function(tab){
        				tab.loader.load();
        			}
        			},
            title: 'Help',
            bodyStyle:"background-image:url(images/texture.jpg); background-repeat: repeat;"
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
	        width: 180,
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
	    			var center=mappa.getCenter();
	    			google.maps.event.trigger(mappa, "resize");
	    			mappa.setCenter(center);
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
	            	html: '<center> <img src="../MAL.png" height="70px" width="300px" alt="logo"/> </center> ',
	            	bodyStyle:"background-image:url(images/texture.jpg) !important; background-repeat: repeat;"
	            },
	            {
	            	xtype:'panel',
	            	layout:'border',
	            	border:false,
	            	minHeight: 380,
	            	minWidth: 600,
	            	style: {
            			split: true,
            	        marginLeft: 'auto',
            	        marginRight: 'auto'
	            	},
	            	items: [{
	            			xtype: 'panel',
	            			region: 'west',
	            	    	collapsible: true,
	            	    	minHeight: 300,
	            	    	minWidth: 150,
	            	        items:[leftPanel]
	            			},mainPanel],
	            	anchor: '80%, -80'
	            }
	]
	    //renderTo: targetRender
	});
	
	Ext.EventManager.onWindowResize(function () {
		accordionh=((Ext.getBody().getViewSize().height) - 243);
		accordionPanel.setHeight(accordionh);
    });
});