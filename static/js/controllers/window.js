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
              componentName: 'RunManager',
              componentState: { templateId: 'run_manager_wrapper' }
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

  window.layout.registerComponent( 'ESGF', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    window.layout.emit('new_window', templateHtml, container );
    container.getElement().html( templateHtml );
  });
  window.layout.registerComponent( 'CDAT', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    window.layout.emit('new_window', templateHtml, container );
    container.getElement().html( templateHtml );
  });
  window.layout.registerComponent( 'RunManager', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    window.layout.emit('new_window', templateHtml, container );
    container.getElement().html( templateHtml );
  });

  window.layout.on( 'initialised', function(){
    angular.bootstrap( document.body, [ 'dashboard' ]);
  });
  window.layout.on( 'stateChanged', function(){
    var state = JSON.stringify( window.layout.toConfig() );
    localStorage.setItem( 'savedState', state );
  });

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
        componentState: { templateId: text }
    };
    window.layout.createDragSource( element, newItemConfig );
  };

  addMenuItem('ESGF', 'esgf_wrapper');
  addMenuItem('CDAT', 'cdat_wrapper');
  addMenuItem('RunManager', 'run_manager_wrapper');

}).call(this);
