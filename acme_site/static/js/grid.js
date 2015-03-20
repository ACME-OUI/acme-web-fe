$('body').ready(function(){


  var gridster;
  var docWidth = $(document).width();
  var docHeight = $(document).height();
  var widgetWidth = 140;
  var widgetHeight = 140;
  var maxCols = Math.floor(docWidth/widgetWidth) - 1;
  var maxHeight = Math.floor(docHeight/widgetHeight);
  var layout = returnBalanced(maxCols, maxHeight);
    // console.log(layout);
    // testLayout(layout);

    // function testLayout(layout) {
    //   for (var i = layout.length - 1; i >= 0; i--) {
    //     for (var j = layout[i].length - 1; j >= 0; j--) {
    //       console.log(i + ' ' + j + ' ' + layout[i][j].row(maxHeight) + ' ' + layout[i][j].col(maxCols) + ' ' + layout[i][j].sizex(maxCols) + ' ' + layout[i][j].sizey(maxHeight));
    //     };
    //   };
    // }


    var resize_handle_html = '<span class="gs-resize-handle gs-resize-handle-both"></span>';

    // Define a widget
    var header1 = ''; 
    var header2 = '';
    var header3 = '';
    var contents = '';
    var optionContents = '';
    header1 += '<div class="grid-panel panel-default">';
    header1 += ' <div class="grid-panel-heading">';
    header1 += '  <div class="panel-header-title text-center">';
    header1 += '    <button type="button" class="btn btn-default btn-xs options" style="float:left;">';
    header1 += '     <span class="fa fa-cog" aria-label="Options"></span>';
    header1 += '    </button>';
    header1 += '    <button type="button" class="btn btn-default btn-xs remove"  style="float:right;">';
    header1 += '     <span class="fa fa-times" aria-label="Close"></span>';
    header1 += '    </button>';
    header1 += '     <p style="text-align: center">';
    // Widget Name
    header2 += '     <p>';
    header2 += '   </div>';
    header2 += '  </div>';
    header2 += ' </div>';
    header2 += ' <div class="panel-body live-tile blue" data-direction="horizontal" data-mode="slid">';
    //header2 += '  <div class="box">&nbsp</div><br>';
    // Widget Contents
    contents += '  <p>The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men.</p>';
    header3 += ' </div>';
    header3 += '</div>';



    var dragStartX = 0;
    var dragStartY = 0;
    var dragStartSizeX = 0;
    var dragStartSizeY = 0;
    var dragStartId = '';
    var dragStartOffset = {
      top: 0,
      left: 0
    };
    var widgetMargins = 1;
    var resizeStartSizeX = 0;
    var resizeStartSizeY = 0;
    var resizeStartX = 0;
    var resizeStartY = 0;


  //Setup the gridster object
  gridster = $(".gridster ul").gridster({
    widget_margins: [widgetMargins, widgetMargins],
    widget_base_dimensions: [widgetWidth, widgetHeight],
    max_cols: maxCols,
    min_cols: maxCols,
    min_rows: maxHeight,
    resize: {
      enabled: true,
      stop: function(e, ui, widget) {
        resizeFixup(e, ui, widget[0].id);
      },
      start: function(e, ui, widget) {
        resizeStartX = parseInt($('#'+widget[0].id).attr('data-col'));
        resizeStartY = parseInt($('#'+widget[0].id).attr('data-row'));
        resizeStartSizeX = parseInt($('#'+widget[0].id).attr('data-sizex'));
        resizeStartSizeY = parseInt($('#'+widget[0].id).attr('data-sizey'));
      }
    },
    draggable: {
      distance: 0,
      limit: true,
      stop: function(e, ui, col, row) {
        dragFixup(e, ui, col, row);
      },
    }
  }).data('gridster');

  gridster.set_dom_grid_height(maxHeight*widgetHeight);

  $('.slide-btn').each(function(){
    $(this).click(function(){
      add_grid($(this).attr('id'));
    });
  });


  /**
   * Registers call backs for window creation buttons
   */
   function add_grid(name){
    // optionContents = '<select>';
    // optionContents+= ' <option value="alpha">Alpha<option>';
    // optionContents+= ' <option value="beta">Beta<option>';
    // optionContents+= ' <option value="charlie">Charlie<option>';
    // optionContents+= ' <option value="delta">Delta<option>';
    // optionContents+= '</select>';
    // optionContents+= '<form oninput="x.value=parseInt(a.value)+parseInt(b.value)">0';
    // optionContents+= ' <input type="range" id="a" value="50">100';
    // optionContents+= ' +<input type="number" id="b" value="50">';
    // optionContents+= ' =<output name="x" for="a b"></output>';
    // optionContents+= '</form>';
    if($('#' + name + '_window').length == 0) {
      var widget_t = ['<li id=' + name + '_window>' + header1 + name + header2 +/* '<div>' + optionContents + '</div><div>' + contents + '</div>' */+ header3 +'</li>',1,1];
      var w = gridster.add_widget.apply(gridster,widget_t);

      //Setup the live tile for the options menu
      $(w).find('.live-tile').liveTile({ direction:'horizontal' });

      //Stop the body from being able to drag
      $(w).find('.panel-body').mousedown(function (event) {
        event.stopPropagation();
      });

      $(w).find('.grid-panel-heading').mousedown(function(event){
        dragStartId = w[0].id;
        var grid = $('#' + dragStartId);
        dragStartX = grid.attr('data-col');
        dragStartY = grid.attr('data-row');
        dragStartSizeX = grid.attr('data-sizex');
        dragStartSizeY = grid.attr('data-sizey');
        dragStartOffset = grid.offset();
        // dragStartOffset.left -= 6;
      });

      $(w).find('.remove').click(function(e) {
        gridster.remove_widget($(w), true);
        setTimeout(function(){ new_window_fixup(); }, 600);
      });

      $(w).find('.options').click(function(e) {
        $(w).find('.live-tile').liveTile('play', 0);
        //widgetOptions(e.target.parentElement.parentElement.parentElement.parentElement);
      });

      new_window_fixup();
    }
  }
  
  /**
   * Brings up the options for the widget
   * widget -> the widget requesting its options
   */
   function widgetOptions(id){

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
  * Computes and sets the size for each window after a resize event
  */
  // function resizeFixup(e, ui, id) {
  //   var i = 0;
  //   var windows = $(".gs-w");
  //   for(; i < windows.length; i++) {

  //   }
  // }

  function move_grid($widget, new_wgd){
    $widget.removeClass('player-revert');
    //update coords instance attributes
    $widget.data('coords').update({
        width: (new_wgd.size_x * gridster.options.widget_base_dimensions[0] +
            ((new_wgd.size_x - 1) * gridster.options.widget_margins[0]) * 2),
        height: (new_wgd.size_y * gridster.options.widget_base_dimensions[1] +
            ((new_wgd.size_y - 1) * gridster.options.widget_margins[1]) * 2)
    });

    $widget.attr({
        'data-col': new_wgd.col,
        'data-row': new_wgd.row,
        'data-sizex': new_wgd.size_x,
        'data-sizey': new_wgd.size_y
    });
  }

  /**
   * Fixes the window positions after a drag event
   * col, row -> the ending col and row of the dragged element
   */
   function dragFixup(e, ui, col, row) {

    var targetId = idFromLocation(col, row);
    var targetX = parseInt($('#'+targetId).attr('data-col'));
    var targetY = parseInt($('#'+targetId).attr('data-row'));
    var targetSizeX = parseInt($('#'+targetId).attr('data-sizex'));
    var targetSizeY = parseInt($('#'+targetId).attr('data-sizey'));
    var targetGrid = $('#'+targetId);
    var startGrid = $('#'+dragStartId);
    if(targetId == dragStartId) {
      startGrid.offset({
        top: dragStartOffset.top ,
        left: dragStartOffset.left
      });
    } else {
      var startOffset = startGrid.offset();
      var targetOffset = targetGrid.offset();
      startGrid.attr({
        'data-col': targetGrid.attr('data-col'),
        'data-row': targetGrid.attr('data-row'),
        'data-sizex': targetGrid.attr('data-sizex'),
        'data-sizey': targetGrid.attr('data-sizey')
      });
      startGrid.offset({
        top: targetOffset.top,
        left: targetOffset.left
      });
      targetGrid.attr({
        'data-col': dragStartX,
        'data-row': dragStartY,
        'data-sizex': dragStartSizeX,
        'data-sizey': dragStartSizeY
      });
      setTimeout(function(){
        targetGrid.offset({
          top: dragStartOffset.top,
          left: dragStartOffset.left
        });
      }, 200);
       
    }
  }

  /**
   * Recomputes and then places each window in its correct position
   * widget -> x, y, id
   */
   function new_window_fixup() {
    var windows = $('.gs-w');
    for (var i = 0; i < windows.length; i++) {
      $(windows[i]).attr({
        'data-col': layout[windows.length-1][i].col(maxCols),
        'data-row': layout[windows.length-1][i].row(maxHeight),
        'data-sizex': layout[windows.length-1][i].sizex(maxCols),
        'data-sizey': layout[windows.length-1][i].sizey(maxHeight)
      });
    };
    gridster.set_dom_grid_height();
    gridster.set_dom_grid_width();
  }

/**
 * returns the layout specifications for a balanced layout
 * canvasSizeX, canvasSizeY are the size of the grid canvas
 * --> Im only doing this for 9 grids right now until I get the names for the next 3
 */
 function returnBalanced(canvasSizeX, canvasSizeY){

  return [
    [{ //1 grid
      row:function(canvasSizeY){
        return 1;
      },
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeY){
        return canvasSizeX;
      },
      sizey:function(canvasSizeY){
        return canvasSizeY;
      },
    }],
    [{ //2 grids
      row:function(canvasSizeY){
        return 1;
      },
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2);
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        return canvasSizeY;
      },
    },{
      row:function(canvasSizeY){
        return 1;
      },
      col:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2+1;
        }
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        return canvasSizeY;
      },
    }],
    [{ //3 grids
      row:function(canvasSizeY){
        return 1;
      }, //top
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeY){
        return canvasSizeX;
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2);
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2+1;
        }
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    }],
    [{ //4 grids
      row:function(canvasSizeY){
        return 1;
      }, //top left
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2);
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){
        return 1;
      }, //top right
      col:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2+1;
        }
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2);
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ // bottom right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2+1;
        }
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    }],
    [{ //5 grids
      row:function(canvasSizeY){
        return 1;
      }, //top left
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2);
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){
        return 1;
      }, //top right
      col:function(canvasSizeX){ 
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2+1;
        }
      },
      sizex:function(canvasSizeX){
        if(canvasSizeX%2 != 0){
          return Math.floor(canvasSizeX/2)+1;
        } else {
          return canvasSizeX/2;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom middle
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1;
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)*2+1;
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    }],
    [{ //6 grids
      row:function(canvasSizeY){
        return 1;
      }, //top left
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){
        return 1;
      }, // top middle
      col:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1;
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){
        return 1;
      }, //top right
      col:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(2*canvasSizeX/3);
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeY){
        return 1;
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom middle
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1;
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)*2+1;
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    }],
    [{ //7 grids
      row:function(canvasSizeX){
        return 1;
      }, //top left
      col:function(canvasSizeX){
        return 1;
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeX){
        return 1;
      }, // top middle left
      col:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)+1;
        } else {
          return canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },
    {
      row:function(canvasSizeX){
        return 1;
      }, // top middle right
      col:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)*2+1;
        } else {
          return 2*canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },
    {
      row:function(canvasSizeX){
        return 1;
      }, //top right
      col:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)*3+1;
        } else {
          return 3*canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)+canvasSizeX%4;
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },
    {
      row:function(canvasSizeY){//bottom left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        return 1;
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },
    {
      row:function(canvasSizeY){//bottom middle
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){//bottom middle
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1;
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },
    {
      row:function(canvasSizeY){//bottom right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)*2+1;
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    }],
    [{ //8 grids
      row:function(canvasSizeX){
        return 1
      }, //top left
      col:function(canvasSizeX){
        return 1
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeX){
        return 1
      }, //top middle left
      col:function(canvasSizeX){//bottom middle
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)+1;
        } else {
          return canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeX){
        return 1
      }, //top middle right
      col:function(canvasSizeX){
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)*2+1;
        } else {
          return 2*canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeX){
        return 1
      }, // top right
      col:function(canvasSizeY){
        if(canvasSizeY%4 != 0){
          return Math.floor(canvasSizeY/4)*3+1;
        } else {
          return 3*canvasSizeY/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)+canvasSizeX%4;
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2);
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        return 1
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom middle left
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)+1;
        } else {
          return canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom middle right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)*2+1;
        } else {
          return 2*canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4);
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    },{
      row:function(canvasSizeY){ //bottom right
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)*3+1;
        } else {
          return 3*canvasSizeX/4+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%4 != 0){
          return Math.floor(canvasSizeX/4)+canvasSizeX%4;
        } else {
          return canvasSizeX/4;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%2 != 0){
          return Math.floor(canvasSizeY/2)+1;
        } else {
          return canvasSizeY/2;
        }
      }
    }],
    [{ //9 grids
      row:function(canvasSizeY){ //top left
        return 1
      }, 
      col:function(canvasSizeX){
        return 1
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3);
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ //top middle
        return 1
      }, 
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3);
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ //top right
        return 1
      }, 
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)*2+1;
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3);
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ // middle left
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)+1;
        } else {
          return canvasSizeY/3+1;
        }
      },
      col:function(canvasSizeX){
        return 1
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3);
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ // middle middle
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)+1;
        } else {
          return canvasSizeY/3+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1;
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3);
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ // middle right
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)+1;
        } else {
          return canvasSizeY/3+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)*2+1;
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3);
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ // bottom left
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)*2+1;
        } else {
          return 2*canvasSizeY/3+1;
        }
      },
      col:function(canvasSizeX){
        return 1
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)+canvasSizeY%3;
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ // bottom middle
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)*2+1;
        } else {
          return 2*canvasSizeY/3+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+1;
        } else {
          return canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3);
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)+canvasSizeY%3;
        } else {
          return canvasSizeY/3;
        }
      }
    },{
      row:function(canvasSizeY){ // bottom right
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)*2+1;
        } else {
          return 2*canvasSizeY/3+1;
        }
      },
      col:function(canvasSizeX){
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)*2+1;
        } else {
          return 2*canvasSizeX/3+1;
        }
      },
      sizex:function(canvasSizeX){ 
        if(canvasSizeX%3 != 0){
          return Math.floor(canvasSizeX/3)+canvasSizeX%3;
        } else {
          return canvasSizeX/3;
        }
      },
      sizey:function(canvasSizeY){
        if(canvasSizeY%3 != 0){
          return Math.floor(canvasSizeY/3)+canvasSizeY%3;
        } else {
          return canvasSizeY/3;
        }
      }
    }]
    ];
  }



});

