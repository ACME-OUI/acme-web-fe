$('body').ready(function(){
    
  	var gridster;

	gridster = $(".gridster ul").gridster({
	    widget_margins: [10, 10],
	    widget_base_dimensions: [140, 140],
	    min_cols: 6,
	    resize: {
	        enabled: true
	    },
      draggable: {
        stop: function(e, ui, $widget) {
          sizeFixup();
        }
      },
	   	max_size_x: 5,
	}).data('gridster');


	$('#provenance').click(function(){
  		add_grid('provenance');
  	});
  $('#status').click(function(){
      add_grid('status');
    });
  $('#science').click(function(){
      add_grid('science');
    });
  $('#nodeList').click(function(){
      add_grid('nodeList');
    });
  $('#heatMap').click(function(){
      add_grid('heatMap');
    });
  $('#modelRun').click(function(){
      add_grid('modelRun');
    });
  $('#nodeSelect').click(function(){
      add_grid('nodeSelect');
    });
  $('#cdat').click(function(){
      add_grid('cdat');
    });
  $('#charting').click(function(){
      add_grid('charting');
    });
  

  	function add_grid(name){
      if($('#' + name + '_window').length == 0) {
        var widget = ['<li id=' + name + '_window></li>',1,1];
    		gridster.add_widget.apply(gridster,widget);
        $("#" + name).bind
      }
      sizeFixup();
  	}

    function sizeFixup() {
      var i = 0;
      var windows = $(".gs-w");
      for(; i < windows.length; i++) {
        var nodesInCol = 0;
        var nodesInRow = 0;
        var j = 0;
        for(; j < windows.length; j++) { 
          if ($(windows[i]).attr('id') != $(windows[j]).attr('id')) {
            if( $(windows[i]).attr('data-row') == $(windows[j]).attr('data-row') 
                || ($(windows[i]).attr('data-row') <= $(windows[j]).attr('data-row')+$(windows[j]).attr('data-sizey') 
                      && $(windows[i]).attr('data-row') >= $(windows[j]).attr('data-row') ) ) {
              console.log("Window " + $(windows[i]).attr('id') + " is in the same row as window " + $(windows[j]).attr('id'));
              nodesInRow++;
            }
            if($(windows[i]).attr('data-col') == $(windows[j]).attr('data-col')) {
              nodesInCol++;
            }
          }
        }
      }
    }

});



/*

-> Provenance Capture
-> Staus Messages
-> Science Input
-> Heat Map
-> CDATWeb
-> ESGF Nodes
-> Model Run
-> Node Selector
-> Charting System Status

*/