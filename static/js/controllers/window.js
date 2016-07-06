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
              componentName: 'ESGF',
              componentState: { templateId: 'esgf_wrapper' }
          },{
              type: 'component',
              componentName: 'CDAT',
              componentState: { templateId: 'cdat_wrapper' }
          },{
              type: 'component',
              componentName: 'Velo',
              componentState: { templateId: 'velo_wrapper' }
          }]
      }]
  }
  window.layout = undefined;
  var savedState = localStorage.getItem( 'savedState' );
  if( savedState !== null ) {
      window.layout = new window.GoldenLayout( JSON.parse( savedState ), $('#layoutContainer') );
  } else {
      window.layout = new window.GoldenLayout( GoldenLayoutConfig, $('#layoutContainer') );
  }

  var addMenuItem = function( title, text ) {
    var element = $( '<li>' + title + '</li>' );
    $( '#menuContainer' ).append( element );

    var newItemConfig = {
        title: title,
        type: 'component',
        componentName: title,
        componentState: { templateId: text }
    };

    window.layout.createDragSource( element, newItemConfig );
  };

  window.layout.registerComponent( 'ESGF', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    window.layout.emit('new_window', templateHtml, container );
    container.getElement().html( templateHtml );
  });
  window.layout.registerComponent( 'CDAT', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    container.getElement().html( templateHtml );
  });
  window.layout.registerComponent( 'Velo', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    container.getElement().html( templateHtml );
  });

  window.layout.on( 'initialised', function(){
    angular.bootstrap( document.body, [ 'dashboard' ]);
  });
  window.layout.on( 'stateChanged', function(){
    var state = JSON.stringify( window.layout.toConfig() );
    localStorage.setItem( 'savedState', state );
  });
  // layout.on( 'new_window', function(template){
  //   console.log(template);
  // });
  window.layout.init();

  addMenuItem('ESGF', 'esgf_wrapper');
  addMenuItem('CDAT', 'cdat_wrapper');
  addMenuItem('Velo', 'velo_wrapper');

}).call(this);
