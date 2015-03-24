$(document).ready(function(){


/****************************************
 	Setup variables
 ***************************************/
	var docWidth = $(".wrapper").width();
	var docHeight = $(".wrapper").height();
	var tileWidth = 100;
	var tileHeight = 100;
	var maxCols = Math.floor(docWidth/tileWidth);
	var maxHeight = Math.floor(docHeight/tileHeight);
	var tiles = [];
	var resize_handle_html = '<span class="gs-resize-handle gs-resize-handle-both"></span>';
		// Define a widget
	var header1 = ''; 
	var header2 = '';
	var header3 = '';
	var contents = '';
	var optionContents = '';
	header1 += '<div class="tile-panel panel-default">';
	header1 += ' <div class="tile-panel-heading">';
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
	header2 += ' <div class="tile-panel-body" data-direction="horizontal" data-mode="slid">';
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

	//i = cols, j = rows
	var board = new Array(maxCols);
	//setup the empty board
	for (var i = board.length - 1; i >= 0; i--) {
		board[i] = new Array(maxHeight);
		for (var j = board[i].length - 1; j >= 0; j--) {
			board[i][j] = {
				occupied: 0,
				tile: ''
			};
		}
	}
/****************************************
 	End setup variables
 ***************************************/
	
	//set the window creation buttons
	$('.slide-btn').each(function(){
	    $(this).click(function(){
	    	var name = $(this).attr('id');
	      	if($('#' + name + '_window').length == 0) {
				var new_tile = '<li id="' + name + '_window" class="tile">' + header1 + name + header2 + contents + header3 +'</li>';
				add_tile(new_tile, name+'_window');
			}
	    });
	});

	function add_tile(html, id){
		$('.tile-holder').append(html);
		var w = $('#'+id);
		$(w).css("display", "none");
		$(w).draggable({
			containment: ".wrapper",
			stop: function(event, ui){
				var pos = grid_from_offset(ui.position);
				dragFixup(pos.col, pos.row);
			}
		});
		tiles.push($(w).attr('id'));

	 	//Setup the live tile for the options menu
	 	$(w).find('.live-tile').liveTile({ direction:'horizontal' });

		//Stop the body from being able to drag
		$(w).find('.panel-body').mousedown(function (event) {
			event.stopPropagation();
		});

		$(w).find('.tile-panel-heading').mousedown(function(event){
			dragStartId = w[0].id;
			var grid = $('#' + dragStartId);
			dragStartX = parseInt(grid.attr('col'));
			dragStartY = parseInt(grid.attr('row'));
			dragStartSizeX = parseInt(grid.attr('sizex'));
			dragStartSizeY = parseInt(grid.attr('sizey'));
			dragStartOffset = grid.offset();
		});

		$(w).find('.remove').click(function(e) {
			$('#'+id).remove();
			for (var i = tiles.length - 1; i >= 0; i--) {
				if(tiles[i] == id){
					tiles.splice(i, 1);
					break;
				}
			};
			positionFixup();
		});

		$(w).find('.options').click(function(e) {

		});
		
		positionFixup();
		
		$(w).fadeIn();
		return w;
	};

	/**
	* Fixes the positions for all windows
	*/
	function positionFixup(){
		for (var i = tiles.length - 1; i >= 0; i--) {
			var layout = returnBalanced(maxCols, maxHeight);
			var t = $('#'+tiles[i]);
			t.attr({
				'row': layout[tiles.length-1][i].row(maxHeight),
				'col': layout[tiles.length-1][i].col(maxCols),
				'sizex': layout[tiles.length-1][i].sizex(maxCols),
				'sizey': layout[tiles.length-1][i].sizey(maxHeight)
			});
			var tile_offset = offset_from_location(parseInt(t.attr('row')), parseInt(t.attr('col')));
			t.css({
				"top": tile_offset.top,
				"left":tile_offset.left,
				"width":t.attr('sizex')*tileWidth,
				"height":t.attr('sizey')*tileHeight});
			update_board(tiles[i]);
		};
	}


	/**
	 * Updates the board to match the tile
	 * id -> the id of the tile to update the board info for
	 */
	function update_board(id){
		var t = $('#'+id);
		for (var k = parseInt(t.attr('col'))-1; k < (parseInt(t.attr('col'))+parseInt(t.attr('sizex'))-1); k++) {
			for (var j = parseInt(t.attr('row'))-1; j < (parseInt(t.attr('row'))+parseInt(t.attr('sizey'))-1); j++) {
				board[k][j].occupied = 1;
				board[k][j].tile = id;
			};
		};
	}

	/**
	* Gives the offset of the tile from row and col
	* row -> the row of the tile
	* col -> the col of th tile
	*/
	function offset_from_location(row, col){
		var offset = $('.tile-board').offset();
		offset.left += (col-1)*tileWidth;
		offset.top += (row-1)*tileHeight;
		return offset;
	}

	/**
   * Fixes the window positions after a drag event
   * col, row -> the ending col and row of the dragged element
   */
   function dragFixup(col, row) {

	    var targetId = board[col-1][row-1].tile;
	    var targetX = parseInt($('#'+targetId).attr('col'));
	    var targetY = parseInt($('#'+targetId).attr('row'));
	    var targetSizeX = parseInt($('#'+targetId).attr('sizex'));
	    var targetSizeY = parseInt($('#'+targetId).attr('sizey'));
	    var targetGrid = $('#'+targetId);
	    var startGrid = $('#'+dragStartId);
	    if(targetId == dragStartId) {
	      var targetOffset = offset_from_location(row,col);
	      $('#'+targetId).css({
	      	'top':dragStartOffset.top,
	      	'left':dragStartOffset.left
	      });
	    } else {
	      var startOffset = offset_from_location(dragStartSizeY, dragStartSizeX);
	      var targetOffset = offset_from_location(targetX, targetY);
	      startGrid.attr({
	        'col': targetGrid.attr('col'),
	        'row': targetGrid.attr('row'),
	        'sizex': targetGrid.attr('sizex'),
	        'sizey': targetGrid.attr('sizey')
	      });
	      startGrid.css({
	      	'top':targetOffset.top,
	      	'left':targetOffset.left,
	      	'width':parseInt(startGrid.attr('sizex'))*tileWidth,
	      	'height':parseInt(startGrid.attr('sizey'))*tileHeight
	      });
	      update_board(dragStartId);

	      targetGrid.attr({
	        'col': dragStartX,
	        'row': dragStartY,
	        'sizex': dragStartSizeX,
	        'sizey': dragStartSizeY
	      });
	      targetGrid.css({
	      	'top':dragStartOffset.top,
	      	'left':dragStartOffset.left,
	      	'width':parseInt(targetGrid.attr('sizex'))*tileWidth,
	      	'height':parseInt(targetGrid.attr('sizey'))*tileHeight
	      });
	      update_board(targetId);
	    }
	}


	/**
	 * Returns the row and col of an element from its offset
	 * pos -> the position of the object
	 */
	function grid_from_offset(pos){
		var location = {
			col: Math.floor(pos.left/tileWidth) + 1,
			row: Math.floor(pos.top/tileHeight) + 1
		}
		return location;
	}
});

