$('body').ready(function(){
    
  	var gridster;
    var maxCols = 6;

	gridster = $(".gridster ul").gridster({
	    widget_margins: [10, 10],
	    widget_base_dimensions: [140, 140],
	    min_cols: 6,
	    resize: {
        enabled: true,
        stop: function(e, ui, $widget) {
          sizeFixup();
        }
	    },
      draggable: {
        stop: function(e, ui, $widget) {
          sizeFixup();
        }
      },
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
      var widget = ['<li id=' + name + '_window>' + name + '</li>',1,1];
  		gridster.add_widget.apply(gridster,widget);
      $("#" + name).bind
    }
    sizeFixup();
	}

  function sizeFixup() {
    var i = 0;
    var windows = $(".gs-w");
    for(; i < windows.length; i++) {
      var nodesInCol = 1;
      var nodesInRow = 1;
      var j = 0;
      for(; j < windows.length; j++) { 
        if (i != j) {
          if( parseInt($(windows[i]).attr('data-row')) == parseInt($(windows[j]).attr('data-row')) 
              || ( parseInt($(windows[i]).attr('data-row'))-1 <= parseInt($(windows[j]).attr('data-row'))-2+parseInt($(windows[j]).attr('data-sizey')) 
                  && parseInt($(windows[i]).attr('data-row')) >= parseInt($(windows[j]).attr('data-row')) ) ) 
          {
            //console.log($(windows[i]).attr('id') + " is in the same row as " + $(windows[j]).attr('id'));
            nodesInRow++;
          }
          if(parseInt($(windows[i]).attr('data-col')) == parseInt($(windows[j]).attr('data-col'))
              || (parseInt($(windows[i]).attr('data-col'))-1 <= parseInt($(windows[j]).attr('data-col'))-2+parseInt($(windows[j]).attr('data-sizex'))
                  && parseInt($(windows[i]).attr('data-col')) >= parseInt($(windows[j]).attr('data-col')) ) ) 
          {
            //console.log($(windows[i]).attr('id') + " is in the same col as " + $(windows[j]).attr('id'));
            nodesInCol++;
          }
        }
      }
      console.log($(windows[i]).attr('id') + ' has ' + nodesInRow + ' other nodes in its row');
      console.log($(windows[i]).attr('id') + ' has ' + nodesInCol + ' other nodes in its col');
     // resize_widget($(windows[i]), )
      if ( ($(windows[i]).attr('data-col')-1) % (maxCols/nodesInRow) != 0 && nodesInRow < 4) {
        console.log('moving ' + $(windows[i]).attr('id') + ' to ' + (parseInt($(windows[i]).attr('data-col'))+(Math.floor(maxCols/nodesInRow) - (parseInt($(windows[i]).attr('data-col'))-1)%Math.floor(maxCols/nodesInRow))));
        if (nodesInRow == 1) {
          var newCol = 1;
        } else {
          newCol = parseInt($(windows[i]).attr('data-col'))+(Math.floor(maxCols/nodesInRow) - (parseInt($(windows[i]).attr('data-col'))-1)%Math.floor(maxCols/nodesInRow));
        }
        gridster.mutate_widget_in_gridmap($(windows[i]), {
          size_x: parseInt($(windows[i]).attr('data-sizex')),
          size_y: parseInt($(windows[i]).attr('data-sizey')),
          col: parseInt($(windows[i]).attr('data-col')),
          row: parseInt($(windows[i]).attr('data-row'))
        }, {
          size_x: parseInt($(windows[i]).attr('data-sizex')),
          size_y: parseInt($(windows[i]).attr('data-sizey')),
          col: newCol,
          row: parseInt($(windows[i]).attr('data-row'))
        });
      }
      get_rows_cols({
      id: $(windows[i]).attr('id'),
      x: parseInt($(windows[i]).attr('data-col')),
      y: parseInt($(windows[i]).attr('data-row')),
      sizex: parseInt($(windows[i]).attr('data-sizex')),
      sizey: parseInt($(windows[i]).attr('data-sizey'))
    });
    }
  }

  /*
    widget -> x, y, sizex, sizey

    returns the number of widgets to the left, right, above, and below the requested widget
    left = left of *any* of the widget of interest cells
  */
  function get_rows_cols(widget) {
    var nodes = {
      left: 0,
      right: 0,
      up: 0, //above the widget on the page, lower row number
      down: 0 //below the widget on the page, higher row number
    };
    var windows = $('.gs-w');
    var i = 0;
    var highestRow = 0;
    for( i = 0; i < windows.length; i++) {
      if(parseInt($(windows[i]).attr('data-row')) + parseInt($(windows[i]).attr('data-sizey')) > highestRow ) {
        highestRow = parseInt($(windows[i]).attr('data-row')) + parseInt($(windows[i]).attr('data-sizey'));
      }
    }
    var j = 0;
    for(; j < widget.x; j++) { //scan to the left of the widget.x position
      if( gridster.is_widget(j, widget.y)) {
        nodes.left++;
      }
    }
    for(j = widget.x + widget.sizex; j <= maxCols; j++) {
      if( gridster.is_widget(j, widget.y)) {
        nodes.right++;
      }
    }
    for(j = widget.y-1 ; j > 0; j--) {
      if( gridster.is_widget(widget.x, j)) {
        nodes.up++;
      }
    }
    for(j = widget.y + widget.sizey; j < highestRow; j++) {
      if( gridster.is_widget(widget.x, j)) {
        nodes.down++;
      }
    }
    
    
    console.log("id:" + widget.id);
    console.log(" up:" + nodes.up);
    console.log(" down:" + nodes.down);
    console.log(" left:" + nodes.left);
    console.log(" right:" + nodes.right);
    return nodes;
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