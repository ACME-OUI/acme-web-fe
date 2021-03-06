(function(){
     console.log("[+] Initializing window system");
     var GoldenLayoutConfig = {
         settings:{
             hasHeaders: true
         },
         content:[{
             type: 'row',
             content: [{
                 type: 'component',
                 componentName: 'DataManager',
                 componentState: {
                    templateId: 'data_manager_wrapper'
                 }
             },{
                 type: 'component',
                 componentName: 'vCDAT',
                 componentState: {
                   templateId: 'cdat_wrapper'
                 }
             },{
                 type: 'component',
                 componentName: 'RunManager',
                 componentState: {
                   templateId: 'run_manager_wrapper'
                 }
             },{
                 type: 'component',
                 componentName: 'Notifications',
                 componentState: {
                   templateId: 'notification_manager_wrapper'
                 }
             }]
         }]
     }
     window.layout = undefined;
     var savedState = localStorage.getItem( 'savedState' );
     if( savedState !== null ) {
         window.layout = new window.GoldenLayout( JSON.parse( savedState ), '#layoutContainer' );
     } else {
         window.layout = new window.GoldenLayout( GoldenLayoutConfig, '#layoutContainer' );
     }

     window.layout.registerComponent( 'DataManager', function( container, state ){
        var templateHtml = $( '#' + state.templateId ).html();
        var element = container.getElement();
        state.module = 'data_manager';
        element.html( templateHtml );
        angular
          .module( state.module )
          .value( 'container', container )
          .value( 'state', state );

        // Actually kick off Angular's magic
        angular.bootstrap( element[ 0 ], [ state.module ] );
     });
     window.layout.registerComponent( 'vCDAT', function( container, state ){
       var templateHtml = $( '#' + state.templateId ).html();
       var element = container.getElement();
       state.module = 'cdat';
       element.html( templateHtml );
       angular
         .module( state.module )
         .value( 'container', container )
         .value( 'state', state );

       // Actually kick off Angular's magic
       angular.bootstrap( element[ 0 ], [ state.module ] );
     });
     window.layout.registerComponent( 'RunManager', function( container, state ){
       var templateHtml = $( '#' + state.templateId ).html();
       var element = container.getElement();
       state.module = 'run_manager';
       element.html( templateHtml );
       angular
         .module( state.module )
         .value( 'container', container )
         .value( 'state', state );

       // Actually kick off Angular's magic
       angular.bootstrap( element[ 0 ], [ state.module ] );
     });
     window.layout.registerComponent( 'Notifications', function( container, state ){
        var templateHtml = $( '#' + state.templateId ).html();
        var element = container.getElement();
        state.module = 'notification_manager';
        element.html( templateHtml );
        angular
          .module( state.module )
          .value( 'container', container )
          .value( 'state', state );

        // Actually kick off Angular's magic
        angular.bootstrap( element[ 0 ], [ state.module ] );
     });

     window.layout.on( 'initialised', function(){
        //angular.bootstrap( document.body, [ 'dashboard' ]);
     });
     window.layout.on( 'stateChanged', function(){
        var state = JSON.stringify( window.layout.toConfig() );
        localStorage.setItem( 'savedState', state );
     });
     window.layout.init();

    $(window).resize(function(event){
      if(window.layout){
         window.layout.updateSize();
      }
    });

    var addMenuItem = function( title, text ) {
      var element = $( '<li>' + title + '</li>' );
      $( '#menuContainer' ).append( element );

     var newItemConfig = {
         title: title,
         type: 'component',
         componentName: title,
         componentState: {
           templateId: text,
         }
     };
     window.layout.createDragSource( element, newItemConfig );
   };

   addMenuItem('DataManager', 'data_manager_wrapper');
   addMenuItem('vCDAT', 'cdat_wrapper');
   addMenuItem('RunManager', 'run_manager_wrapper');
   addMenuItem('Notifications', 'notification_manager_wrapper');

 }).call(this);
