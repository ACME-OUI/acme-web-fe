$('body').ready(function(){
    
  	var gridster;
    var maxCols = 6;
    var maxHeight = 6;
    var resize_handle_html = '<span class="gs-resize-handle gs-resize-handle-both"></span>'

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
  

  /**
   * Registers call backs for window creation buttons
   */
	function add_grid(name){
    if($('#' + name + '_window').length == 0) {
      var widget = ['<li id=' + name + '_window></li>',1,1];
  		gridster.add_widget.apply(gridster,widget);
      $('#' + name).bind
    }
    sizeFixup();
	}

  /**
  * Computes and sets the size for each window
  */
  function sizeFixup() {
    var i = 0;
    var windows = $(".gs-w");
    for(; i < windows.length; i++) {
      var nodesInCol = 1;
      var nodesInRow = 1;
      var j = 0;
      get_windows({
        id: $(windows[i]).attr('id'),
        x: parseInt($(windows[i]).attr('data-col')),
        y: parseInt($(windows[i]).attr('data-row')),
      });
     // resize_widget($(windows[i]), )
      if ( ($(windows[i]).attr('data-col')-1) % (maxCols/nodesInRow) != 0 && nodesInRow < 4) {
        //console.log('moving ' + $(windows[i]).attr('id') + ' to ' + (parseInt($(windows[i]).attr('data-col'))+(Math.floor(maxCols/nodesInRow) - (parseInt($(windows[i]).attr('data-col'))-1)%Math.floor(maxCols/nodesInRow))));
        if (nodesInRow == 1) {
          var newCol = 1;
        } else {
          newCol = parseInt($(windows[i]).attr('data-col'))+(Math.floor(maxCols/nodesInRow) - (parseInt($(windows[i]).attr('data-col'))-1)%Math.floor(maxCols/nodesInRow));
        }
        /*
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
*/
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



  /**
   * Recomputes and then places each window in its correct position
   */
  function re_place_windows() {
    var windows = $('.gs-w');
    for (var i = windows.length - 1; i >= 0; i--) {
      nodes = get_rows_cols({
        x: parseInt($(windows[i]).attr('data-col')),
        y: parseInt($(windows[i]).attr('data-row')),
        sizex: parseInt($(windows[i]).attr('data-sizex')),
        sizey: parseInt($(windows[i]).attr('data-sizey'))
      });

    };
  }

  /**
   * returns the number unique windows to the left, right, above, and below the given widget
   * widget -> x, y, id
   */
  function get_windows(widget) {
    var nodesInCol = 0;
    var nodesInRow = 0;
    var windows = $('gs-w');
    for(var j = 0; j < windows.length; j++) { 
      if (widget.id != $(windows[j]).attr('id')) {
        if( widget.x == parseInt($(windows[j]).attr('data-row')) 
            || ( widget.x-1 <= parseInt($(windows[j]).attr('data-row'))-2+parseInt($(windows[j]).attr('data-sizey')) 
                && widget.y >= parseInt($(windows[j]).attr('data-row')) ) ) 
        {
          //console.log($(windows[i]).attr('id') + " is in the same row as " + $(windows[j]).attr('id'));
          nodesInRow++;
        }
        if(widget.y == parseInt($(windows[j]).attr('data-col'))
            || (widget.y-1 <= parseInt($(windows[j]).attr('data-col'))-2+parseInt($(windows[j]).attr('data-sizex'))
                && widget.y >= parseInt($(windows[j]).attr('data-col')) ) ) 
        {
          //console.log($(windows[i]).attr('id') + " is in the same col as " + $(windows[j]).attr('id'));
          nodesInCol++;
        }
      }
    }
    var newHTML = '<div><p>' + widget.id + '</p><p>nodesInRow:' + nodesInRow + '</p><p>nodesInCol:' + nodesInCol + '</p></div>';
    $('#'+widget.id).html(newHTML);
    //console.log(widget.id + ' has ' + nodesInRow + ' other nodes in its row and ' + nodesInCol + ' in its col');
  }


  /**
   * returns the number of widgets to the left, right, above, and below the requested widget
   * left = left of *any* of the widget of interest cells
   * widget -> x, y, sizex, sizey
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
    var newHTML = $('#'+widget.id).html() + '<p>Up:' + nodes.up + '</p><p>Right:' + nodes.right + '</p><p>Down:' + nodes.down + '</p><p>Left:' + nodes.left + '</p>' + resize_handle_html;
    $('#'+widget.id).html(newHTML);
    return nodes;
  }

});


