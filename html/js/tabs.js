Ext.require('Ext.tab.*');

Ext.onReady(function(){
    // basic tabs 1, built from existing content
    var tabs = Ext.createWidget('tabpanel', {
        renderTo: 'container',
        layout: 'fit',
        activeTab: 0,
        defaults :{
            bodyPadding: 0
        },
        items: [{
            contentEl:'mia_mappa', 
            title: 'Mappa'
        },{
            contentEl:'prova', 
            title: 'Tabella'
        }]
    });
});