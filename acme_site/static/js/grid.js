$('body').ready(function(){
    
    var gridster;
    var maxCols = 6;
    var maxHeight = 4;
    var resize_handle_html = '<span class="gs-resize-handle gs-resize-handle-both"></span>';
    var header1 = '<div class="panel panel-default">';
    header1 +=    '   <div class="panel-heading hidden-box">';
    header1 +=    '    <div class="panel-header-title text-center">';
    header1 +=    '      <div class="pull-left">';
    header1 +=    '        <button class="btn btn-default btn-sm" data-toggle="modal" data-target="#widgetRemove">';
    header1 +=    '          <i class="fa fa-cog fa-spin">Settings</i>';
    header1 +=    '        </button>';
    header1 +=    '      </div>';
    //                    <!-- Widget Name-->
    var header2 = '      <div class="pull-right">';
    header2    += '         <button class="btn btn-default " data-toggle="modal" data-target="#widgetConfig">';
    header2    += '           <span class="glyphicon glyphicon-align-justify"></span>';
    header2    += '             </button></div></div></div><div class="panel-body"><!-- Panel Body --></div></div>';

    var dragStartX = 0;
    var dragStartY = 0;
    var dragStartSizeX = 0;
    var dragStartSizeY = 0;
    var dragStartId = '';
    var dragStartOffset = {
      top: 0,
      left: 0
    };



    /* Define a widget
    var widget = '<div class="panel panel-default">';
    widget += ' <div class="panel-heading hidden-box">';
    widget += '  <div class="panel-header-title text-center">';
    widget += '   <div class="pull-left">';
    widget += '   <button class="btn btn-default btn-xs" data-toggle="modal" data-target="#widgetConfiguration">';
    widget += '    <span class="glyphicon glyphicon-align-justify"></span>';
    widget += '   </button>';
    widget += '   </div>';
    widget += '   Widget';
    widget += '   <div class="pull-right">';
    widget += '    <button class="btn btn-default btn-xs" data-toggle="modal" data-target="#widgetRemove">';
    widget += '     <span class="glyphicon glyphicon-remove"></span>';
    widget += '    </button>';
    widget += '   </div>';
    widget += '  </div>';
    widget += ' </div>';
    widget += ' <div class="panel-body">';
    widget += '  <div class="box">&nbsp</div>';
    widget += '  Lorem ipsum dolor sit amet, consectetur adipiscing elit.';
    widget += '  <input type="text" style="width: 200px" id="i" />';
    widget += ' </div>';
    widget += '</div>';
    */

  gridster = $(".gridster ul").gridster({
      widget_margins: [10, 10],
      widget_base_dimensions: [140, 140],
      max_cols: maxCols,
      min_cols: maxCols,
      resize: {
        enabled: true,
        stop: function(e, ui, $widget) {
          //resizeFixup(e, ui);
        }
      },
      draggable: {
        start: function(e, ui, id) {
          dragStartId = id[0].id;
          var grid = $('#' + dragStartId);
          var offset = grid.offset();
          dragStartX = grid.attr('data-col');
          dragStartY = grid.attr('data-row');
          dragStartSizeX = grid.attr('data-sizex');
          dragStartSizeY = grid.attr('data-sizey');
          dragStartOffset.top = offset.top;
          dragStartOffset.left = offset.left;
          console.log('drag starting at left:' + dragStartOffset.left + ' top:' + dragStartOffset.top);
        },
        stop: function(e, ui, col, row) {
          dragFixup(e, ui, col, row);
        },
        drag: function(e, ui, id) {
          //dragFixup(e, ui, id);
        }
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
  

  function dragFixup(e, ui, col, row) {
    //$($('.gs-w')[0]).offset({top: 100});
    console.log("col:" + col + " row:" + row);
    console.log(idFromLocation(col, row));
    var targetId = idFromLocation(col, row);
    var targetX = parseInt($('#'+targetId).attr('data-col'));
    var targetY = parseInt($('#'+targetId).attr('data-row'));
    var targetSizeX = parseInt($('#'+targetId).attr('data-sizex'));
    var targetSizeY = parseInt($('#'+targetId).attr('data-sizey'));
    var startGrid = $('#'+dragStartId);
    var targetGrid = $('#'+targetId);
    if(targetId == dragStartId) {
      console.log('Putting back ' + targetId + ' where it started');
      gridster.mutate_widget_in_gridmap(
        targetGrid,
        {
          col: targetGrid.attr('data-col'),
          row: targetGrid.attr('data-row'),
          size_x: targetGrid.attr('data-sizex'),
          size_y: targetGrid.attr('data-sizey'),
        },
        {
          col: dragStartX,
          row: dragStartY,
          size_x: dragStartSizeX,
          size_y: dragStartSizeY,
        });
      var targetOffset = targetGrid.offset();
      console.log('placing ' + dragStartId + ' at left:' + dragStartOffset.left + ' top:' + dragStartOffset.top);
      if(dragStartOffset.left != targetOffset.left && dragStartOffset.top != targetOffset.top) {
          startGrid.offset({
            top: dragStartOffset.top,
            left: dragStartOffset.left
          });
        }
    } else {
      console.log('Switching ' + dragStartId + ' with ' + targetId);
      var startOffset = startGrid.offset();
      var targetOffset = targetGrid.offset();
      gridster.mutate_widget_in_gridmap(
        startGrid,
        {
          col: startGrid.attr('data-col'),
          row: startGrid.attr('data-row'),
          size_x: startGrid.attr('data-sizex'),
          size_y: startGrid.attr('data-sizey'),
        },
        {
          col: targetGrid.attr('data-col'),
          row: targetGrid.attr('data-row'),
          size_x: targetGrid.attr('data-sizex'),
          size_y: targetGrid.attr('data-sizey'),
        });
      gridster.mutate_widget_in_gridmap(
        targetGrid,
        {
          col: targetGrid.attr('data-col'),
          row: targetGrid.attr('data-row'),
          size_x: targetGrid.attr('data-sizex'),
          size_y: targetGrid.attr('data-sizey'),
        },
        {
          col: dragStartX,
          row: dragStartY,
          size_x: dragStartSizeX,
          size_y: dragStartSizeY,
        });
    }
    console.log('placing ' + dragStartId + ' at left:' + targetOffset.left + ' top:' + targetOffset.top);
    startGrid.offset({
      top: targetOffset.top,
      left: targetOffset.left
    });
    
      

  }


  //this only works when going up and to the left
  //  TODO: add the sizex and sizey so it works going down and to the right
  function idFromLocation(col, row, sizex, sizey) {
    var windows = $('.gs-w');
    var id;
    for (var i = windows.length - 1; i >= 0; i--) {
      if(parseInt($(windows[i]).attr('data-row')) <= row && row <= ( parseInt($(windows[i]).attr('data-row'))+parseInt($(windows[i]).attr('data-sizey'))-1) )  
      {
        if(parseInt($(windows[i]).attr('data-col')) <= col && col <= (parseInt($(windows[i]).attr('data-col'))+parseInt($(windows[i]).attr('data-sizex'))-1) ) 
        {
          id = $(windows[i]).attr('id');
          return id;
        }
      }
      
    };
  }


  /**
   * Registers call backs for window creation buttons
   */
  function add_grid(name){
    var widget = '<p>' + name + '</p>'
    if($('#' + name + '_window').length == 0) {
      var widget_t = ['<li id=' + name + '_window>' + widget + '</li>',1,1];
      gridster.add_widget.apply(gridster,widget_t);
      //$('#' + name).bind
      new_window_fixup({id: name + '_window'});
    }
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
   * widget -> x, y, id
   */
  function new_window_fixup(widget) {
    var windows = $('.gs-w');
    if (windows.length == 1) {
      gridster.mutate_widget_in_gridmap(
        $(windows[0]),
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
    } else {

      //find the largest widget
        //then find the largest widets major axis, cut it in half and place the new widget in the space
      var largetsWidget = 0;
      var largetsWidgetIndex = 0;
      for (var i = windows.length - 1; i >= 0; i--) {
        var currentWidget = parseInt($(windows[i]).attr('data-sizex')) * parseInt($(windows[i]).attr('data-sizey'));
        if( currentWidget > largetsWidget ) {
          largetsWidget = currentWidget;
          largetsWidgetIndex = i;
        }
      }
      if(parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')) >= parseInt($(windows[largetsWidgetIndex]).attr('data-sizex'))  ) {
        var newHeight = parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')) / 2;
        if(Math.floor(parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')) / 2) != parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')) / 2) {
          newHeight = Math.floor(parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')) / 2) + 1;
        }
        gridster.mutate_widget_in_gridmap(
          $(windows[largetsWidgetIndex]),
          {
            col: parseInt($(windows[largetsWidgetIndex]).attr('data-col')),
            row: parseInt($(windows[largetsWidgetIndex]).attr('data-row')),
            size_x: parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')),
            size_y: parseInt($(windows[largetsWidgetIndex]).attr('data-sizey'))
          },
          {
            col: parseInt($(windows[largetsWidgetIndex]).attr('data-col')),
            row: parseInt($(windows[largetsWidgetIndex]).attr('data-row')),
            size_x: parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')),
            size_y: Math.floor(parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')) / 2)
          });
        gridster.mutate_widget_in_gridmap(
          $('#' + widget.id),
          {
            col: parseInt($('#' + widget.id).attr('data-col')),
            row: parseInt($('#' + widget.id).attr('data-row')),
            size_x: parseInt($('#' + widget.id).attr('data-sizex')),
            size_y: parseInt($('#' + widget.id).attr('data-sizey'))
          },
          {
            col: parseInt($(windows[largetsWidgetIndex]).attr('data-col')),
            row: parseInt($(windows[largetsWidgetIndex]).attr('data-row')) + parseInt($(windows[largetsWidgetIndex]).attr('data-sizey')),
            size_x: parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')),
            size_y: newHeight
          });
      } else {
        var newWidth = parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')) / 2;
        if(Math.floor(parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')) / 2) != parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')) / 2) {
          newWidth = Math.floor(parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')) / 2) + 1;
        }
        gridster.mutate_widget_in_gridmap(
          $(windows[largetsWidgetIndex]),
          {
            col: parseInt($(windows[largetsWidgetIndex]).attr('data-col')),
            row: parseInt($(windows[largetsWidgetIndex]).attr('data-row')),
            size_x: parseInt($(windows[largetsWidgetIndex]).attr('data-sizex')),
            size_y: parseInt($(windows[largetsWidgetIndex]).attr('data-sizey'))
          },
          {
            col: parseInt($(windows[largetsWidgetIndex]).attr('data-col')),
            row: parseInt($(windows[largetsWidgetIndex]).attr('data-row')),
            size_x: Math.floor(parseInt($(windows[largetsWidgetIndex]).attr('data-sizex'))/2),
            size_y: parseInt($(windows[largetsWidgetIndex]).attr('data-sizey'))
          });

        gridster.mutate_widget_in_gridmap(
          $('#' + widget.id),
          {
            col: parseInt($('#' + widget.id).attr('data-col')),
            row: parseInt($('#' + widget.id).attr('data-row')),
            size_x: parseInt($('#' + widget.id).attr('data-sizex')),
            size_y: parseInt($('#' + widget.id).attr('data-sizey'))
          },
          {
            col: (parseInt($(windows[largetsWidgetIndex]).attr('data-col')) + parseInt($(windows[largetsWidgetIndex]).attr('data-sizex'))),
            row: parseInt($(windows[largetsWidgetIndex]).attr('data-row')),
            size_x: newWidth,
            size_y: parseInt($(windows[largetsWidgetIndex]).attr('data-sizey'))
          });
        console.log('moving ' + widget.id + ' to x:' + (parseInt($(windows[largetsWidgetIndex]).attr('data-col')) + parseInt($(windows[largetsWidgetIndex]).attr('data-sizex'))) + ' y:' + parseInt($(windows[largetsWidgetIndex]).attr('data-row')));
        
      }    
    }
    gridster.set_dom_grid_height();
    gridster.set_dom_grid_width();
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


