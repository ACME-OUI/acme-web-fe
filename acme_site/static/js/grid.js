$('body').ready(function(){
    
  	var gridster;
    var maxCols = 6;
    var maxHeight = 4;
    var resize_handle_html = '<span class="gs-resize-handle gs-resize-handle-both"></span>'

	gridster = $(".gridster ul").gridster({
	    widget_margins: [10, 10],
	    widget_base_dimensions: [140, 140],
	    max_cols: maxCols,
      min_cols: maxCols,
	    resize: {
        enabled: true,
        stop: function(e, ui, $widget) {
          resizeFixup(e, ui);
        }
	    },
      draggable: {
        stop: function(e, ui, $widget) {
          dragFixup(e, ui);
        },
      },
	}).data('gridster');

  gridster.set_dom_grid_height(642);
  //gridster.set_dom_grid_width(maxCols);


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
  

  function dragFixup() {

  }


  /**
   * Registers call backs for window creation buttons
   */
	function add_grid(name){
    if($('#' + name + '_window').length == 0) {
      var widget = ['<li id=' + name + '_window></li>',1,1];
  		gridster.add_widget.apply(gridster,widget);
      $('#' + name).bind
    }
    new_window_fixup();
	}

  /**
  * Computes and sets the size for each window
  */
  function sizeFixup(e, ui) {
    var i = 0;
    var windows = $(".gs-w");
    for(; i < windows.length; i++) {
      var j = 0;
      var rowsCols = get_windows({
        id: $(windows[i]).attr('id'),
        x: parseInt($(windows[i]).attr('data-col')),
        y: parseInt($(windows[i]).attr('data-row')),
      });
      var nodes = get_rows_cols({
        id: $(windows[i]).attr('id'),
        x: parseInt($(windows[i]).attr('data-col')),
        y: parseInt($(windows[i]).attr('data-row')),
        sizex: parseInt($(windows[i]).attr('data-sizex')),
        sizey: parseInt($(windows[i]).attr('data-sizey')),
      });
    }
  }



  /**
   * Recomputes and then places each window in its correct position
   * widget -> x, y, id, sizex, sizey, nodesInRow, nodesInCol, occupiedLeft, occupiedRight, occupiedUp, occupiedDown
   */
  function new_window_fixup(e, ui) {
    var windows = $('.gs-w');
    var rowArray = [];
    var smallestRow;
    var smallestSize
    if (windows.length == 1) {
      rowArray.push(1);
      gridster.mutate_widget_in_gridmap($(windows[0]),
      {
        col: 1,
        row: 1,
        size_x: 1,
        size_y: 1
      },
      {
        col: 1,
        row: 1,
        size_x: maxCols,
        size_y: maxHeight
      });
      gridster.set_dom_grid_height();
      gridster.set_dom_grid_width();
    } else {
      //check to see if we need to create a new row
      //maxCol is the size of the row with the most columns
      var maxCol = 1;
      for (i = 0; i < rowArray.length; i++) {
        if (rowArray[i] > maxCol) {
          maxCol = rowArray[i];
        }
      }
      //if the largest row is larger then the
      //number of rows, add a new row
      if (maxCol > rowArray.length) {
        //new row is needed
        rowArray.push(0); //add the new row size to the rowArray
        smallestRow = rowArray.length-1;
        smallestSize = 1;
      } else {
        smallestRow = rowArray[0];//index of the smallest row
        smallestSize = maxCols+1; //value of the smallest row
        for (i = rowArray.length - 1; i >= 0; i--) { //find the index and length of the smallest row
          if (rowArray[i] <= smallestSize) {
            smallestRow = i;
            smallestSize = rowArray[i];
          }
        }
      }
      gridster.mutate_widget_in_gridmap($(windows[i]), //move the grid to the correct row/col
      {
        x: parseInt($(windows[i]).attr('data-col')),
        y: parseInt($(windows[i]).attr('data-row')),
        size_x: parseInt($(windows[i]).attr('data-sizex')),
        size_y: parseInt($(windows[i]).attr('data-sizey'))
      },{
        x: smallestRow,
        y: smallestSize,
        size_x: parseInt($(windows[i]).attr('data-sizex')),
        size_y: parseInt($(windows[i]).attr('data-sizey'))
      });
      
      rowArray[smallestRow] ++;
      
      for (i = 0; i < windows.length; i++) {
        /*If the grid is in the smallest row
        if (parseInt($(windows[i]).attr('data-row'))-1 == smallestRow) { 
          gridster.mutate_widget_in_gridmap(
            $(windows[i]),
            {
              x: parseInt($(windows[i]).attr('data-col')),
              y: parseInt($(windows[i]).attr('data-row')),
              size_x: parseInt($(windows[i]).attr('data-sizex')),
              size_y: parseInt($(windows[i]).attr('data-sizey'))
            },{
              x: parseInt($(windows[i]).attr('data-col')),
              y: parseInt($(windows[i]).attr('data-row')),
              size_x: Math.floor(maxCols / rowArray[smallestRow]),
              size_y: Math.floor(maxHeight / rowArray.length),
          });
        }*/
      
        if (parseInt($(windows[i]).attr('data-col')) != 1) {
          for(var j = 0; j < panelArray.length; j++) {
            if ((panelArray[j].data('pos').row == panelArray[i].data('pos').row) && (panelArray[j].data('pos').col == (panelArray[i].data('pos').col -1 ) )) {
              var offset = panelArray[j].offset();
              break;
            }
          }
          panelArray[i].offset({
            left: offset.left+panelArray[i].width(), 
            top: panelArray[i].parent().offset().top + (panelArray[i].data('pos').row * panelArray[i].height() ) });
        } else if (panelArray[i].data('pos').col == 0 && panelArray[i].data('pos').row != 0) {
          panelArray[i].offset({
            top: panelArray[i].parent().offset().top + (panelArray[i].data('pos').row * panelArray[i].height() ) });
        }
      }
      for (i = 0; i < rowArray.length; i++) {
        if (rowArray[i] % 2 != 0 && rowArray[i] % 3 != 0 && rowArray[i] != 1) {
          for (j = 0; j < panelArray.length; j++) {
            if (panelArray[j].data('pos').row == i && (panelArray[j].data('pos').col+1) == rowArray[i]) {
              panelArray[j].width(panelArray[j].width() + pixPerGrid);
              break;;
            }
          }
        }
      } 
    }

  }

  /**
   * returns the number unique windows to the left, right, above, and below the given widget
   * widget -> x, y, id
   */
  function get_windows(widget) {
    var nodesInCol = 1;
    var nodesInRow = 1;
    var windows = $('.gs-w');
    for(var j = 0; j < windows.length; j++) { 
      if (widget.id != $(windows[j]).attr('id')) {
        if( widget.y == parseInt($(windows[j]).attr('data-row')) 
            || ( parseInt($(windows[j]).attr('data-row')) <= widget.y 
                && widget.y <= ( parseInt($(windows[j]).attr('data-row'))+parseInt($(windows[j]).attr('data-sizey'))-1) ) ) 
        {
          //console.log($(windows[i]).attr('id') + " is in the same row as " + $(windows[j]).attr('id'));
          nodesInRow++;
        }
        if(widget.x == parseInt($(windows[j]).attr('data-col'))
            || ( parseInt($(windows[j]).attr('data-col')) <= widget.x 
                && widget.x <= (parseInt($(windows[j]).attr('data-col'))+parseInt($(windows[j]).attr('data-sizex'))-1) ) )
        {
          //console.log($(windows[i]).attr('id') + " is in the same col as " + $(windows[j]).attr('id'));
          nodesInCol++;
        }
      }
    }
    var newHTML = '<div><p>' + widget.id + '</p><p>nodesInRow:' + nodesInRow + '</p><p>nodesInCol:' + nodesInCol + '</p></div>';
    $('#'+widget.id).html(newHTML);
    return {
      row: nodesInRow,
      col: nodesInCol
    };
  }


  /**
   * returns the number of widgets to the left, right, above, and below the requested widget
   * left = left of *any* of the widget of interest cells
   * widget -> x, y, sizex, sizey

   * TODO: Make sure it scans to the left no only from the origin of the node, but to the left
          of each grid it extends down, and like wise for right, down, up
   */
  function get_rows_cols(widget) {
    var nodes = {
      left: 0,
      right: 0,
      up: 0, //above the widget on the page, lower row number
      down: 0 //below the widget on the page, higher row number
    };
    var windows = $('.gs-w');
    var highestRow = 1;
    for( var i = 0; i < windows.length; i++) {
      if(parseInt($(windows[i]).attr('data-row')) + parseInt($(windows[i]).attr('data-sizey')) > highestRow ) {
        highestRow = parseInt($(windows[i]).attr('data-row')) + parseInt($(windows[i]).attr('data-sizey'));
      }
    }
    for( var j = 1; j < widget.x; j++) { //scan to the left of the widget.x position
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


