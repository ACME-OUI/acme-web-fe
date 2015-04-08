$(document).ready(function(){


/****************************************
 	Setup variables
 ***************************************/
	var docWidth = $(".tile-board").width();
	var docHeight = $(".tile-board").height();
	var tileWidth = 100;
	var tileHeight = 100;
	var maxCols = Math.floor(docWidth/tileWidth);
	var maxHeight = Math.floor(docHeight/tileHeight);
	$('.wrapper').width(maxCols*tileWidth);
	$('.tile-board').css({'height':maxHeight*tileHeight});
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
    var resizeDir = '';

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




	/**
	 * Creates a new tile window and rearranges all the other tiles to make room 
	 * html-> the content of the tile
	 * id-> the name for the new tile to take
	 * options-> whatever new options i decided to add, right now a x,y,sizex,sizey to handle window sizes
	 * callback-> an optional function to pass that will be called with add_tile is done
	 */
	function add_tile(html, id, options, callback){
		$('.tile-holder').append(html);
		var w = $('#'+id);
		$(w).css({
			'display': 'none',
			'z-index': 1
		});

		$(w).draggable({
			//containment: '.tile-board',
			helper: 'clone',
			start: function(event, ui){

				ui.helper.addClass('ui-draggable-dragging-no-transition');
				ui.helper.animate({
					'opacity':'0.5',
					'z-index':10,
					'width':'20%',
					'height':'20%',
				});
			},
			stop: function(event, ui){
				
				var pos = grid_from_offset(ui.position);
				dragFixup(pos.col, pos.row);
				$(ui.helper).css({
					'opacity':'1.0',
					'z-index':1,
				});
			},
			cursorAt: {
				left:200, 
				top:15
			}, 
		});

		$(w).resizable({
			handles: 'n, w, e, s', 
			animate: true,
			animateDuration: 'fast',
			animateEasing: 'easeOutQuint',
			// containment: '.wrapper',
			helper: 'ui-resizable-helper',
			grid: [tileWidth, tileHeight],
			start: function(event, ui){
				resizeStartX = parseInt(ui.element.attr('col'));
				resizeStartSizeX = parseInt(ui.element.attr('sizex'));
				resizeStartY = parseInt(ui.element.attr('row'));
				resizeStartSizeY = parseInt(ui.element.attr('sizey'));
			},
			resize: function(event, ui){

			},
			stop: function(event, ui){
				resizeFixup(ui);
				var el = ui.element;
				setTimeout(function(el){
					if(resizeDir == 'n' && parseInt(el.attr('row')) == 1){
						el.css({
							'top':$('.tile-board').offset().top,
							'height':tileHeight*parseInt(el.attr('sizey')),
							'width':tileWidth*parseInt(el.attr('sizex'))
						});
					}
					else if(resizeDir == 's'){
						el.css({
							'height':tileHeight*parseInt(el.attr('sizey')),
							'width':tileWidth*parseInt(el.attr('sizex'))
						});
					}
					else if(resizeDir == 'e' && parseInt(el.attr('col'))+parseInt(el.attr('sizex'))-1 == maxCols){
						el.css({
							'left': tileWidth*(parseInt(el.attr('col'))-1)+$('.tile-holder').offset().left,
							'width': tileWidth*parseInt(el.attr('sizex')),
							'height':tileWidth*parseInt(el.attr('sizey'))
						});

					}
					else if(resizeDir == 'w' && parseInt(el.attr('col')) == 1){
						el.css({
							'width':tileWidth*parseInt(el.attr('sizex')),
							'height':tileWidth*parseInt(el.attr('sizey')),
							'left':$('.tile-board').offset().left
						});
					}
					else{
						el.css({
							'left':(parseInt(el.attr('col'))-1)*tileWidth+$('.tile-holder').offset().left,
							'height':parseInt(el.attr('sizey'))*tileHeight,
							'width':parseInt(el.attr('sizex'))*tileWidth
						});
					} 
				}, 500, el);
			}
		});

		$(w).find('.ui-resizable-n').mousedown(function(){
			resizeDir = 'n';
		});
		$(w).find('.ui-resizable-s').mousedown(function(){
			resizeDir = 's';
		});
		$(w).find('.ui-resizable-e').mousedown(function(){
			resizeDir = 'e';
		});
		$(w).find('.ui-resizable-w').mousedown(function(){
			resizeDir = 'w';
		});

		tiles.push($(w).attr('id'));

	 	//Setup the live tile for the options menu
	 	$(w).find('.live-tile').liveTile({ direction:'horizontal' });

		//Stop the body from being able to drag
		$(w).find('.tile-panel-body').mousedown(function (event) {
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
		if(options != null){
			$(w).attr({
      		'row': options.y,
      		'col': options.x,
      		'sizex': options.sizex,
      		'sizey': options.sizey
	      	});
	      	$(w).css({
	      		'top': options.y*tileHeight,
	      		'left': (options.x -1)*tileWidth + $('.tile-holder').offset().left,
	      		'width': options.sizex*tileWidth,
	      		'height': options.sizey*tileHeight
	      	});
		} else {
			positionFixup();
		}
		update_board(id);
		if($('body').attr('class') == 'night'){
			$(w).find('.tile-panel-body').css({
	          'background-color': '#0C1021;',
	          'border-color': '#00f;',
	          'color': '#fff'
	        });
		}
		$(w).fadeIn();
		if(callback != null)
			callback();
		return $(w);
	};


	/**
	 * A recursive function to fix windows adjacent to windows being dragged up
	 * moved -> an set of windows already moved
	 * dir -> the direction it moved. up, down, right, left
	 * diff -> the amount of grid spaces the window resized
	 * side -> the side of the window being resized. n, s, e, w (the side this call should resize, not the original window)
	 * id -> the id of the window this call should resize
	 */

	 function recursiveResize(moved, dir, diff, side, id){
	 	var curWindow = $('#'+id);
	 	var x = parseInt(curWindow.attr('col'));
	 	var y = parseInt(curWindow.attr('row'));
	 	var sizex = parseInt(curWindow.attr('sizex'));
	 	var sizey = parseInt(curWindow.attr('sizey'));
	 	if(dir == 'up'){
	 		if(side == 'n'){
	 			var adj = new Set();
		 		for (var i = x; i < x + sizex; i++) {
					 adj.add(board[i-1][y - 2].tile);
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'row':y-diff,
					'sizey':sizey+diff
				});
				curWindow.css({
					'top':(y-diff)*tileHeight-40,
					'height':(sizey+diff)*tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, done resizing
					return;
				} else {
					//we need to keep resizing
					recursiveResize(moved, dir, diff, 's', helperReturn.adj.values().next().value);
				}
	 		}
	 		else if(side =='s'){
	 			var adj = new Set();
		 		for (var i = x; i < x + sizex; i++) {
					 adj.add(board[i-1][y + sizey - 1].tile);
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizey':sizey-diff
				});
				curWindow.css({
					'height':(sizey-diff)*tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, all windows have been resized
					return; 
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'n', helperReturn.adj.values().next().value);
				}
	 		} else {
	 			//error
	 			return
	 		}
	 	}
	 	else if(dir == 'down'){
	 		if(side == 'n'){
	 			var adj = new Set();
		 		for (var i = x; i < x + sizex; i++) {
					 adj.add(board[i-1][y - 2].tile);
				};
				//check the base case-> all windows have been moved
				moved.add(id);
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'row':y-diff,
					'sizey':sizey+diff
				});
				curWindow.css({
					'top':(y-diff)*tileHeight-40,
					'height':(sizey+diff)*tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, done resizing
					return;
				} else {
					//we need to keep resizing
					recursiveResize(moved, dir, diff, 's', helperReturn.adj.values().next().value);
				}
	 		}
	 		else if(side =='s'){
	 			var adj = new Set();
		 		for (var i = x; i < x + sizex; i++) {
					 adj.add(board[i-1][y + sizey - 1].tile);
				};
				//check the base case-> all windows have been moved
				moved.add(id);
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizey':sizey-diff
				});
				curWindow.css({
					'height':(sizey-diff)*tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, all windows have been resized
					return; 
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'n', helperReturn.adj.values().next().value);
				}
	 		} else {
	 			//error
	 			return
	 		}
	 	}
	 	else if(dir == 'right'){
			if(side == 'e'){
				var adj = new Set();
		 		for (var i = y; i < y + sizey; i++) {
					 adj.add(board[x + sizex - 1][i - 1].tile);
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizex':sizex-diff
				});
				curWindow.css({
					'width':(sizex-diff)*tileWidth,
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, all windows have been resized
					return; 
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'w', helperReturn.adj.values().next().value);
				}
	 		}
	 		else if(side =='w'){
	 			var adj = new Set();
		 		for (var i = y; i < y + sizey; i++) {
					 adj.add(board[x - 2][i - 1].tile);
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'col':x-diff,
					'sizex':sizex+diff
				});
				curWindow.css({
					'width':(sizex+diff)*tileWidth,
					'left':(x-diff-1)*tileWidth+$('.tile-holder').offset().left
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, all windows have been resized
					return; 
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'e', helperReturn.adj.values().next().value);
				}
	 		} else {
	 			//error
	 			return
	 		}
	 	}
	 	else if(dir == 'left'){
	 		if(side == 'e'){
				var adj = new Set();
		 		for (var i = y; i < y + sizey; i++) {
					 adj.add(board[x + sizex - 1][i - 1].tile);
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizex':sizex-diff
				});
				curWindow.css({
					'width':(sizex-diff)*tileWidth,
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finished == true){
					//base case, all windows have been resized
					return; 
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'w', helperReturn.adj.values().next().value);
				}
	 		}
	 		else if(side =='w'){
	 			var adj = new Set();
		 		for (var i = y; i < y + sizey; i++) {
					 adj.add(board[x - 2][i - 1].tile);
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'col':x-diff,
					'sizex':sizex+diff
				});
				curWindow.css({
					'width':(sizex+diff)*tileWidth,
					'left':(x-diff)*tileWidth-92
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if(helperReturn.finshed == true){
					//base case, all windows have been resized
					return; 
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'e', helperReturn.adj.values().next().value);
				}
	 		} else {
	 			//error
	 			return;
	 		}
	 	} else {
	 		//error
	 		return;
	 	}
	 }

	 /**
	  * Helper to handle checking window adjacency
	  * adj -> Set of adjacent windows
	  * moved -> Set of moved windows
	  * returns if the recurcive function is done, and the new adj
	  */
	  function adjHelper(adj, moved) {
	  	var done = true;
		adj.forEach(function(item){
			if(!moved.has(item)){
				done = false;
			} else {
				adj.delete(item);
			}
		}, moved);

		return {'finished':done, 'adj':adj};
	  }


	  /**
	   * Helper to handle removing an occluded tile from the list of tiles
	   * tile -> the tile to check if it should be removed
	   */
	   function removeHelper(tile){
	   		if(parseInt(tile.attr('sizex')) <= 0 || parseInt(tile.attr('sizey')) <= 0){
				$.when(tile.fadeOut()).then(function(){
						tile.remove();
 				});
 				for (var i = tiles.length - 1; i >= 0; i--) {
					if(tiles[i] == tile.attr('id')){
						tiles.splice(i, 1);
						break;
					}
				};
			}
	   }





	/**
	 * Fixes the position of adjacent tiles after a resize event
	 * ui -> the ui element from the resize event
	 */
	 //TODO: if the n handle of the top element is pulled, move it back. same for w of left, s of bottom, e of right
	 function resizeFixup(ui){
	 	var resizeId = ui.element.attr('id');
	 	//which direction did it resize?
	 	if(resizeDir == 'n'){
	 		var diff = virtical_location(ui.originalPosition.top, 0) - virtical_location(ui.helper.position().top, 0);
	 		if(diff <= 0 && parseInt(ui.element.attr('row')) <= 1){
	 			//the tile is at the top
	 			return;
		 	}
	 		var virt_adj = new Set();
	 		for (var i = resizeStartX; i < resizeStartX + resizeStartSizeX; i++) {
				if(board[i-1][resizeStartY-2].tile != resizeId){
					virt_adj.add(board[i-1][resizeStartY-2].tile);
				}
			};
	 		//did it go up or down?
	 		$(ui.element).attr({
	 			'row':parseInt(ui.element.attr('row'))-diff,
	 			'sizey':parseInt(ui.element.attr('sizey'))+diff
	 		});
	 		update_board(resizeId);
	 		var moved = new Set();
	 		moved.add(resizeId);
	 		if(diff < 0){
	 			//it moved down
	 			virt_adj.forEach(function(item){
					recursiveResize(moved, 'down', diff, 's', item);
	 			});
	 		} 
	 		else if(diff > 0){
	 			//it moved up
	 			virt_adj.forEach(function(item){
	 				recursiveResize(moved, 'up', diff, 's', item);
	 			});
	 		}
	 	}
	 	if(resizeDir == 's'){
	 		var diff = virtical_location(ui.originalPosition.top, ui.originalSize.height) - virtical_location(ui.helper.position().top, ui.helper.height());
	 		if(parseInt(ui.element.attr('row'))+parseInt(ui.element.attr('sizey'))-1 == maxHeight ){
	 			//the tile is at the bottom
	 			return;
	 		}
	 		var virt_adj = new Set();
	 		for (var i = resizeStartX; i < resizeStartX + resizeStartSizeX; i++) {
				if(board[i-1][resizeStartY + resizeStartSizeY - 1].tile != resizeId){
					virt_adj.add(board[i-1][resizeStartY + resizeStartSizeY - 1].tile);
				}
			};
	 		//did it go up or down?
	 		$(ui.element).attr({
	 			'sizey':parseInt(ui.element.attr('sizey'))-diff
	 		});
	 		update_board(resizeId);
	 		var moved = new Set();
	 		moved.add(resizeId);
	 		if( diff < 0){
	 			//it moved down
	 			virt_adj.forEach(function(item){
	 				recursiveResize(moved, 'down', diff, 'n', item);
	 			});
	 		} 
	 		else if(diff > 0){
	 			//it moved up
	 			virt_adj.forEach(function(item){
	 				recursiveResize(moved, 'up', diff, 'n', item);
	 			});
	 		}
	 	} 
	 	if(resizeDir == 'e'){
	 		if(parseInt(ui.element.attr('col'))+parseInt(ui.element.attr('sizex'))-1 == maxCols){
	 			//the element is on the right of the board
	 			return;
	 		}
	 		var horz_adj = new Set();
	 		for (var i = resizeStartY; i < resizeStartY + resizeStartSizeY; i++) {
				if(board[resizeStartX + resizeStartSizeX - 1][i-1].tile != resizeId){
					horz_adj.add(board[resizeStartX + resizeStartSizeX - 1][i-1].tile);
				}
			};
			//did it go right or left?
			var diff = horizontal_location(ui.originalPosition.left, ui.originalSize.width) - horizontal_location(ui.helper.position().left, ui.helper.width());
			ui.element.attr({
	 			'sizex':parseInt(ui.element.attr('sizex'))-diff
	 		});
			update_board(resizeId);
			var moved = new Set();
			moved.add(resizeId);
	 		if( diff < 0){
	 			//it moved right
	 			horz_adj.forEach(function(item){
	 				recursiveResize(moved, 'right', diff, 'w', item);
	 			});
	 		} 
	 		else if(diff > 0){
	 			//it moved left
	 			horz_adj.forEach(function(item){
	 				recursiveResize(moved, 'left', diff, 'w', item);
	 			});
	 		} 
	 	} 
	 	if(resizeDir == 'w'){
	 		if(parseInt(ui.element.attr('col')) == 1){
	 			//the element is on the left side of the board
	 			return;
	 		}
	 		var horz_adj = new Set();
	 		for (var i = resizeStartY; i < resizeStartY + resizeStartSizeY; i++) {
				if(board[resizeStartX - 2][i-1].tile != resizeId){
					horz_adj.add(board[resizeStartX - 2][i-1].tile);
				}
			};
	 		//did it go right or left?
	 		var diff = horizontal_location(ui.originalPosition.left,0) - horizontal_location(ui.helper.position().left, 0);
	 		ui.element.attr({
	 			'col':parseInt(ui.element.attr('col'))-diff,
	 			'sizex':parseInt(ui.element.attr('sizex'))+diff
	 		});
	 		update_board(resizeId);
	 		var moved = new Set();
	 		moved.add(resizeId);
	 		if( diff < 0){
	 			//it moved right

	 			horz_adj.forEach(function(item){
	 				recursiveResize(moved, 'right', diff, 'e', item);
	 			});
	 		} 
	 		else if(diff > 0){
	 			//it moved left
	 			horz_adj.forEach(function(item){
	 				recursiveResize(moved, 'left', diff, 'e', item);
	 			});
	 		} 
	 	}
	 }

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
		for (var k = parseInt(t.attr('col'))-1; k < parseInt(t.attr('col'))+parseInt(t.attr('sizex'))-1; k++) {
			for (var j = parseInt(t.attr('row'))-1; j < parseInt(t.attr('row'))+parseInt(t.attr('sizey'))-1; j++) {
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

		if(col < 0 || col > maxCols || row < 0 || row > maxHeight){
			$('.ui-draggable-dragging').remove();
	    	return;
		}
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
	      	'left':dragStartOffset.left,
	      	'height':dragStartSizeY*tileHeight,
	      	'width':dragStartSizeX*tileWidth
	      });
	    } else {
	      var startOffset = offset_from_location(dragStartSizeY, dragStartSizeX);
	      var targetOffset = offset_from_location(targetY, targetX);
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

	/**
	 * Returns the col from the position and size of an element
	 * x -> the horizontal position of the object
	 * sizex -> the horizontal size of the object
	 */
	function horizontal_location(x, sizex){
		if(((x+sizex)/tileWidth)%1 >= 0.5){
			return Math.ceil((x+sizex)/tileWidth)+1;
		} else {
			return Math.floor((x+sizex)/tileWidth)+1;
		}
	}

	/**
	 * Returns the row from the position and size of an element
	 * y -> the horizontal position of the object
	 * sizey -> the horizontal size of the object
	 */
	function virtical_location(y, sizey){
		if(((y+sizey)/tileHeight)%1 >= 0.5){
			return Math.ceil((y+sizey)/tileHeight)+1
		} else {
			return Math.floor((y+sizey)/tileHeight)+1;
		}
	}


/***********************************
        Left slide menu
***********************************/
	var body = document.body;

	function leftMenuToggle(){
		$('#slide-menu-left').toggle('slide',{
			direction: 'left',
			easing: 'easeOutCubic'}, 500);
		if( $('#toggle-left-a').text() == 'Open Menu') {
			$('#toggle-left-a').text('Close Menu');
		} else {
			$('#toggle-left-a').text('Open Menu');
		}
	}

	$('#toggle-slide-left').click(function(e){
		leftMenuToggle();
	});

	$('#save-layout').click(function(){
		leftMenuToggle();
		var mask = document.createElement('div');
		$(mask).addClass('mask');
		$(mask).attr({'id':'mask'});
		$(mask).click(function(){
			$(this).fadeOut().queue(function(){
				$(this).remove();
				$('.save-layout').remove();
			});
		  
		});
		$('body').append(mask);

		var saveMenu = document.createElement('div');
		$(saveMenu).addClass('bvc');
		$(saveMenu).addClass('save-layout');
		$(saveMenu).attr({'id':'save-menu'});
		var saveMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
		saveMenuHtml += '<form name="save-layout-form" id="save-form">'; 
		saveMenuHtml += 'Layout Name:<br><input type="text" id="layout-name">';
		saveMenuHtml += '<input type="submit" value="Save" id="save-btn">';
		saveMenuHtml += '</form></div><div class="bevel bl br"></div>';
		$(saveMenu).html(saveMenuHtml);
		$('body').append(saveMenu);
		$(mask).fadeIn();
		$('#save-btn').click(function(){
			var layout_name = document.getElementById('layout-name').value;
			var layout = [];
			$('.tile').each(function(){
				layout.push({
					tileName: $(this).attr('id').substr(0, $(this).attr('id').indexOf('_')),
					x: $(this).attr('col'),
					y: $(this).attr('row'),
					sizex:'max-'+(maxCols-parseInt($(this).attr('sizex'))),
					sizey:'max-'+(maxHeight-parseInt($(this).attr('sizey')))
				});
			});
			if($('body').hasClass('night')){
				var mode = 'night';
			} else {
				mode = 'day'
			}
			var data = {
					name: layout_name,
					mode: mode,
					style: 'balanced',
					layout: layout,
				};

			data = JSON.stringify(data);
			var csrfToken = getCookie('csrftoken');
			$.ajaxSetup({
				beforeSend: function(xhr){
					xhr.setRequestHeader('X-CSRFToken', csrfToken);
				}
			});
			$.ajax({
				url:'save_layout/',
				type: 'POST',
				data: data,
				dataType: 'json',
				async: true,
				cache: false,
				statusCode: {
					422: function(){
						alert('Invalid Layout Name');
					},
					500: function(){
						alert('Server Error')
					}

				}
			});
			$('.mask').remove();
			$('.save-layout').remove();
		});
	});


  $('#load-layout').click(function(){
  	var options = {};
  	$.ajax({
  		url: 'load_layout/',
  		type: 'GET',
  		success: function(request){
  			options = jQuery.parseJSON(request);
  			var mask = document.createElement('div');
		    $(mask).addClass('mask');
		    $(mask).attr({'id':'mask'});
		    $(mask).click(function(){
		      fadeOutMask();
		    });
		    $('body').append(mask);
		    var loadMenu = document.createElement('div');
		    $(loadMenu).addClass('bvc');
		    $(loadMenu).addClass('save-layout');
		    var loadMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
		    loadMenuHtml += '<form name="load-layout-form" id="save-form">'; 
		    loadMenuHtml += 'Select Layout:<br><select id="select-layout">';
		    $.each(options, function(k, v){
		    	loadMenuHtml += '<option value="' + v + '">' + v + '</option>';
		    });
		    loadMenuHtml += '</select><input type="submit" value="Load" id="load-button">';
		    loadMenuHtml += '</form></div><div class="bevel bl br"></div>';
		    $(loadMenu).html(loadMenuHtml);
		    $('body').append(loadMenu);
		    $(mask).fadeIn();
		    $('#load-button').click(function(){
				var name = document.forms['load-layout-form'].elements[0].options[document.forms['load-layout-form'].elements[0].selectedIndex].text;
				var csrfToken = getCookie('csrftoken');
				$.ajaxSetup({
					beforeSend: function(xhr){
						xhr.setRequestHeader('X-CSRFToken', csrfToken);
					}
				});
				var data = {'layout_name':name};
				data = JSON.stringify(data);
		     	$.ajax({
			      	url: 'load_layout/',
			      	type: 'POST',
			      	data: data,
			      	dataType: 'json',
			      	success: function(request){
						layout = []
			      		$.each(request.board_layout, function(k, v){
			      			layout.push(layoutFix(v));
			      		});
			      		loadLayout(layout, request.mode);
			      	}
		      });
		    });
  		}
  	});

    $('.tile').each(function(){
  		$(this).remove();
  	});
  	tiles = [];
    leftMenuToggle();
  });

	function layoutFix(layout){

		var x = layout.x.indexOf('max');
		var y = layout.y.indexOf('max');
		var sizex = layout.sizex.indexOf('max');
		var sizey = layout.sizey.indexOf('max');

		if(x != -1){
			if(layout.x.length != 3){
				layout.x = maxCols - parseInt(layout.x.substr(x+4)); 
			} else {
				layout.x = maxCols;
			}
		} else {
			layout.x = parseInt(layout.x);
		}
		if(y != -1){
			if(layout.y.length != 3){
				layout.y = maxHeight - parseInt(layout.y.substr(y+4));
			} else {
				layout.y = maxHeight;
			}
		} else {
			layout.y = parseInt(layout.y);
		}
		if(sizex != -1){
			if(layout.sizex.length != 3){
				layout.sizex = maxCols - parseInt(layout.sizex.substr(sizex+4));
			} else {
				layout.sizex = maxCols;
			}
		} else {
			layout.sizex = parseInt(layout.sizex);
		}
		if(sizey != -1){
			if(layout.sizey.length != 3){
				layout.sizey = parseInt(layout.sizey.substr(sizey+4));
			} else {
				layout.sizey = maxHeight;
			}
		} else {
			layout.sizey = parseInt(layout.sizey);
		}
		
		return layout;
	}

  function loadLayout(layout, mode){
  	fadeOutMask();
    if(mode == 'day'){
      setDay();
    }
    else if(mode == 'night'){
      setNight();
    }

    for(var i = 0; i < layout.length; i++){
    	var name = layout[i].tileName;
    	var new_tile = '<li id="' + name + '_window" class="tile">' + header1 + name + header2 + contents + header3 +'</li>';
      	add_tile(new_tile, name+'_window', {
      		x: layout[i].x,
      		y: layout[i].y,
      		sizex: layout[i].sizex,
      		sizey: layout[i].sizey
      	});
      	

    }
  }

  function fadeOutMask(){
  	$('#mask').fadeOut().queue(function(){
        $('#mask').remove();
        $('.save-layout').remove();
      });
  }

  function setNight(){
    $('body').attr({
        'class':'night'
      });
      $('.tile-panel-body').each(function(){
        $(this).css({
          'background-color': '#0C1021;',
          'border-color': '#00f;',
          'color': '#fff'
        });
      });
      $(body).attr({
        'background-color':'#051451!important',
        'color':'#aaa!important'
      });
      $('#dark-mode-toggle').text('Dark mode is on');
  }

  function setDay(){
    $('body').attr({
        'class':'day'
      });
      $('.tile-panel-body').each(function(){
        $(this).css({
          'background-color': '#fff;',
          'color': '#111;',
          'border-color': '#000;'
        });
      });
      $(body).attr({
        'background-color':'#fff',
        'color':'#000'
      });
      $('#dark-mode-toggle').text('Dark mode is off');
  }


  $('#dark-mode-toggle').click(function(e){
    if($('body').attr('class') == 'day'){
      //turn dark
      setNight();
    } else {
      //turn light
      setDay();
    }
  });

	/**********************************
	       Top slide down menu
	**********************************/

	$('#drop-down-tab').click(function(e){
		var menuHeight = parseInt($('#drop-down-menu').css('height'));
		if($('#drop-down-menu').css('display') == 'none'){
		  $('.tile').each(function(){
		    $(this).css({
		      'top':parseInt($(this).css('top'))+menuHeight
		    });
		  });
		} else {
		  $('.tile').each(function(){
		    $(this).css({
		      'top':parseInt($(this).css('top'))-menuHeight
		    });
		  });
		}
		$('#drop-down-menu').slideToggle('normal');
	});

	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}




});

