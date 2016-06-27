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
  var layout = new window.GoldenLayout(GoldenLayoutConfig, $('#layoutContainer'));

  var addMenuItem = function( title, text ) {
    var element = $( '<li>' + text + '</li>' );
    $( '#menuContainer' ).append( element );

    var newItemConfig = {
        title: title,
        type: 'component',
        componentName: title,
        componentState: { text: text }
    };

    layout.createDragSource( element, newItemConfig );
  };

  layout.registerComponent( 'ESGF', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    container.getElement().html( templateHtml );
  });
  layout.registerComponent( 'CDAT', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    container.getElement().html( templateHtml );
  });
  layout.registerComponent( 'Velo', function( container, state ){
    var templateHtml = $( '#' + state.templateId ).html();
    container.getElement().html( templateHtml );
  });

  layout.on( 'initialised', function(){
    angular.bootstrap( document.body, [ 'dashboard' ]);
  });
  layout.on( 'stateChanged', function(){
    var state = JSON.stringify( layout.toConfig() );
    localStorage.setItem( 'savedState', state );
  });
  layout.init();

  addMenuItem('ESGF', 'ESGF');
  addMenuItem('CDAT', 'CDAT');
  addMenuItem('Velo', 'Velo');

}).call(this);
