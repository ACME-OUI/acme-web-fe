$(document).ready(function(){


/****************************************
 	Setup variables
 	***************************************/
 	// var docWidth = $(".tile-board").width();
 	// var docHeight = $(".tile-board").height();
 	var docHeight, docWidth, maxCols, maxHeight, tileHeight, tileWidth;
 	calcMaxSize();
 	
 	// var tileWidth = 50;
 	// var tileHeight = 50;
 	// var maxCols = Math.floor(docWidth/tileWidth)-1;
 	// var maxHeight = Math.floor(docHeight/tileHeight)-1;
 	$('.wrapper').width(maxCols*tileWidth);
 	$('.wrapper').height(maxHeight*tileHeight);
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
	header2 += '  <div class="tile-contents">'
	// Widget Contents
	contents += '  <p>The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men.</p>';
	header3 += ' </div></div></div>';
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
	var needsFixXBool = true;
	var needsFixYBool = true;
	var fixValX = 99;
	var fixValY = 99;
	var mode = {
		light: 'day'
	}
	boardSetup(maxCols, maxHeight);
	loadDefaultLayout();
	
/****************************************
 	End setup variables
 	***************************************/





 	//find if the user has a default layout, if so load it
 	function loadDefaultLayout(){

 		$.ajax({
 			url: 'load_layout/',
 			type: 'GET',
 			success: function(request){
 				options = jQuery.parseJSON(request);
 				$.each(options, function(k, v){
 					if(v.default == true){
 						for(var i = 0; i < v.layout.length; i++){
 							v.layout[i] = layoutFix(v.layout[i]);
 							if(v.layout[i].x == 1){
 								needsFixXBool = false;
 							} else {
 								if(v.layout[i].x < fixValX){
 									fixValX = v.layout[i].x;
 								}
 							}
 							if(v.layout[i].y == 1){
 								needsFixYBool = false;
 							} else {
 								if(v.layout[i].y < fixValY){
 									fixValY = v.layout[i].y;
 								}
 							}
 						}
 						loadLayout(v.layout, v.mode);
 					}
 				});
 			}
 		});
 	}


 	/**
 	 * A temporary function to deal with some aweful rounding issues
 	 * Hopefully I will solve the problem and I can get rid of this :(
 	 */
 	function windowLoadFix(){
 		var needsFixup = true;
 		var alltiles = $('.tile');
 		$('.tile').each(function(){
 			if(parseInt($(this).attr('col')) == 1){
 				needsFixup == false;
 			}
 		});
 		if(needsFixup){
 			$('.tile').each(function(){
 				$(this).attr('col') = parsetInt($(this).attr('col')) - 1;
 			});
 		}

 	}
 	
 	

 	// Remove extra stuff from the header which isnt going to be used from the dashboard 
 	$('#footer').remove();
 	$('#dashboard-link').remove();
 	$('#uvcdat-link').remove();
 	$('#glubus-link').remove();
 	$('#classic-link').remove();
 	$('#cdatweb-link').remove();

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

	//setup the hander to fix the windows after a resize
	$(window).resize(function() {
		if(event.target == this){
			if(this.resizeTO) clearTimeout(this.resizeTO);
	        this.resizeTO = setTimeout(function() {
	            $(this).trigger('resizeEnd');
	        }, 500);
		}
        
    });

    $(window).bind('resizeEnd', function() {
    	//handleWindowResize();
	});

    $('.node-item').click(function(){
    	if($('#nodeSelect_window').length != 0){
    		$('#nodeSelect_window').find('.tile-contents').empty();
    	} else {
    		var new_tile = '<li id="' + "nodeSelect" + '_window" class="tile">' + header1 + "nodeSelect" + header2 + header3 +'</li>';
    		add_tile(new_tile, "nodeSelect_window");
    	}
    	var nodeName = $(this).find('a').text();
    	populateNodeSelect(nodeName);
    
    });

    function populateNodeSelect(id){
    	var data = {
    		node: id
    	}
    	data = JSON.stringify(data);
    	var csrfToken = getCookie('csrftoken');
    		$.ajaxSetup({
    			beforeSend: function(xhr){
    				xhr.setRequestHeader('X-CSRFToken', csrfToken);
    			}
    		});
    	$.ajax({
			url:'node_info/',
			type: 'POST',
			data: data,
			success: function(response){
				var node_data = jQuery.parseJSON(response);
				$('#nodeSelect_window').find('.tile-contents').append('<table id=node-info></table>');
				for( var key in node_data){
					var data = '<tr><td class="key">' + key + '</td><td class="value">' + node_data[key] + '</td><tr>';
					$('#nodeSelect_window').find('#node-info').append(data);
				}
				$.ajax({
					url:node_data['hostname'],
					type: 'GET',
					success: function(){
						var status = '<tr><td class="key">status</td><td class="value" style="color:green;">UP</td></tr>';
						$('#nodeSelect_window').find('#node-info').append(status);
					},
					statusCode: {
	    				500: function(){
	    					var status = '<tr><td class="key">status</td><td class="value"style="color:red;">DOWN</td></tr>';
							$('#nodeSelect_window').find('#node-info').append(status);
	    				},
	    				404: function(){
	    					var status = '<tr><td class="key">status</td><td class="value" style="color:red;">DOWN</td></tr>';
							$('#nodeSelect_window').find('#node-info').append(status);
	    				}
	    			}

				});
			}
		});
    }



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
	 		'z-index': 1, 
	 		'opacity': 0
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
				handleResizeStart(event, ui);
			},
			resize: function(event, ui){
				event.stopPropagation();
			},
			stop: function(event, ui){
				handleResizeStop(event, ui);
				event.stopPropagation();
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
			// for(var i = 0; i < tiles.length -1; i ++){
			// 	if(id != tiles[i]){
			// 		// if the tile is overlapping in the y direction t.y + t.sizey >= y > t.y
			// 		if(parseInt($('#'+tiles[i]).attr('row'))+parseInt($('#'+tiles[i]).attr('sizey')) - 1 > parseInt($(w).attr('row')) && parseInt($(w).attr('row')) > parseInt($('#'+tiles[i]).attr('row'))){
			// 			$(w).attr({
			// 				'row' : parseInt($('#'+tiles[i]).attr('row'))+parseInt($('#'+tiles[i]).attr('sizey'))
			// 			});
			// 		}
			// 		if(parseInt($('#'+tiles[i]).attr('col'))+parseInt($('#'+tiles[i]).attr('sizex')) - 1 > parseInt($(w).attr('col')) && parseInt($(w).attr('col')) > parseInt($('#'+tiles[i]).attr('col'))){
			// 			$(w).attr({
			// 				'col' : parseInt($('#'+tiles[i]).attr('col'))+parseInt($('#'+tiles[i]).attr('sizex'))
			// 			});
			// 		}
			// 	}
			// }
			update_board(id);
			var tile_offset = offset_from_location(parseInt($(w).attr('row')), parseInt($(w).attr('col')));
			$(w).css({
				"top": tile_offset.top,
				"left":tile_offset.left,
				"width":$(w).attr('sizex')*tileWidth,
				"height":$(w).attr('sizey')*tileHeight
			});
		} else {
			positionFixup();
		}
		if($('body').attr('class') == 'night'){
			$(w).find('.tile-panel-body').css({
				'background-color': '#0C1021;',
				'border-color': '#00f;',
				'color': '#fff'
			});
		}
		$(w).animate({'opacity':1}, 'slow', 'easeOutCubic');

		if(callback != null)
			callback();
		return $(w);
	};

	/**
	 * Handles all actions at the start of a resize event
	 * event -> The event variable
	 * ui -> the ui element handed down from the jquery handler
	 */
	function handleResizeStart(event, ui){
		resizeStartX = parseInt(ui.element.attr('col'));
		resizeStartSizeX = parseInt(ui.element.attr('sizex'));
		resizeStartY = parseInt(ui.element.attr('row'));
		resizeStartSizeY = parseInt(ui.element.attr('sizey'));
		switch(resizeDir){
			case 'n':
				$('#'+ui.element.attr('id')).css({
					'-webkit-transition': 'height 200ms easeOutQuint!important',
				    '-moz-transition': 'height 200ms easeOutQuint!important',
				    '-o-transition': 'height 200ms easeOutQuint!important',
				    '-ms-transition': 'height 200ms easeOutQuint!important',
				    'transition': 'height 200ms easeOutQuint!important',
				});
			case 's':
			case 'e':
			case 'w':
		}
		event.stopPropagation();
	}

	/**
	 * Handles all actions needed at the end of a resize event
	 * event -> The event variable
	 * ui -> the ui element handed down from the jquery handler
	 */
	function handleResizeStop(event, ui){
		resizeFixup(ui);
		var el = ui.element;
		el.css({
			'left':(parseInt(el.attr('col'))-1)*tileWidth+$('.tile-holder').offset().left,
			'height':parseInt(el.attr('sizey'))*tileHeight,
			'width':parseInt(el.attr('sizex'))*tileWidth
		});
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
	 				'top':(y-diff)*tileHeight + $('.navbar').height() - 1,
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
					'top':(y-diff)*tileHeight + $('.navbar').height() - 1,
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
					'left':(x-diff-1)*tileWidth + $('.wrapper').offset().left
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
    	saveMenuHtml += '<input type="submit" value="Save" id="save-btn"><br>';
    	saveMenuHtml += '<input type="checkbox" name="default" value="default" id="default">Default Layout';
    	saveMenuHtml += '</form></div><div class="bevel bl br"></div>';
    	$(saveMenu).html(saveMenuHtml);
    	$('body').append(saveMenu);
    	$(mask).fadeIn();
    	$('#save-btn').click(function(event){
    		event.preventDefault();
    		var layout_name = document.getElementById('layout-name').value;
    		var layout = [];
    		$('.tile').each(function(){
    			layout.push({
    				tileName: $(this).attr('id').substr(0, $(this).attr('id').indexOf('_')),
    				x: parseInt($(this).attr('col'))/maxCols,
    				y: parseInt($(this).attr('row'))/maxHeight,
    				sizex: parseInt($(this).attr('sizex'))/maxCols,
    				sizey: parseInt($(this).attr('sizey'))/maxHeight
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
    			default_layout: document.getElementById('default').checked
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
				//parse response
				options = jQuery.parseJSON(request);
				//create background mask
				var mask = document.createElement('div');
				$(mask).addClass('mask');
				$(mask).attr({'id':'mask'});
				$(mask).click(function(){
					fadeOutMask();
				});
				$('body').append(mask);
				//create load menu and populate with values
				var loadMenu = document.createElement('div');
				$(loadMenu).addClass('bvc');
				$(loadMenu).addClass('save-layout');
				var loadMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
				loadMenuHtml += '<form name="load-layout-form" id="save-form">'; 
				loadMenuHtml += 'Select Layout:<br><select id="select-layout">';
				$.each(options, function(k, v){
					loadMenuHtml += '<option value="' + v.nane + '">' + v.name + '</option>';
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
							$('.tile').each(function(){
								$(this).remove();
							});
							tiles = [];
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
		leftMenuToggle();
	});


	/**
	 * Resolves the size of the layout to match the current page
	 * layout -> the layout for one tile at a time
	 */
	function layoutFix(layout){

		layout.x = checkZero(Math.round(layout.x * maxCols));
		layout.y = checkZero(Math.round(layout.y * maxHeight));
		layout.sizex = checkZero(Math.round(layout.sizex * maxCols));
		layout.sizey = checkZero(Math.round(layout.sizey * maxHeight));
		var diff = layout.x + layout.sizex - 1 - maxCols
		if(diff > 0){
			layout.sizex -= diff;
		}
		diff = layout.y + layout.sizey - 1 - maxHeight;
		if(diff > 0){
			layout.sizey -= diff;
		}
		return layout;
	}


	/**
	 * loads a layout onto the page
	 * layout -> a full layout with all the tiles 
	 * mode -> the day/night mode of the layout
	 */
	function loadLayout(layout, mode){
		fadeOutMask();
		if(mode == 'day'){
			setDay();
		}
		else if(mode == 'night'){
			setNight();
		}
		mode.light = mode

		for(var i = 0; i < layout.length; i++){
			var name = layout[i].tileName;
			var new_tile = '<li id="' + name + '_window" class="tile">' + header1 + name + header2 + contents + header3 +'</li>';
			add_tile(new_tile, name+'_window', {
				x: layout[i].x - needsFixX(),
				y: layout[i].y - needsFixY(),
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
		$('#drop-down-menu').slideToggle();
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

	function calcMaxSize(){
		docHeight = $(window).height() - $('.navbar').height() - 10;
	 	docHeight -= docHeight%10;
	 	docWidth = $(window).width();
	 	docWidth -= docWidth%10;
	 	var dimensionComponents = factor(docHeight).sort(function(a, b){return a.factor - b.factor});
	 	for(var i = 0; i < dimensionComponents.length; i++){
	 		if(dimensionComponents[i].multiplicator % 10 != 0){
	 			dimensionComponents.splice(i, 1);
	 			i--;
	 		}
	 	}
	 	if(dimensionComponents.legnth == 0){
	 		tileHeight = 50;
	 		maxHeight = Math.floor(docHeight)/50;
	 	} else {
		 	dimensionComponents = dimensionComponents[Math.floor(dimensionComponents.length/2)];
		 	tileHeight = dimensionComponents.factor;
		 	maxHeight = dimensionComponents.multiplicator;
	 	}
	 	
	 	dimensionComponents = factor(docWidth).sort(function(a, b){return a.factor - b.factor});
	 	for(var i = 0; i < dimensionComponents.length; i++){
	 		if(dimensionComponents[i].multiplicator % 10 != 0){
	 			dimensionComponents.splice(i, 1);
	 			i--;
	 		}
	 	}
	 	if(dimensionComponents.length == 0){
	 		tileWidth = 50;
	 		maxCols = Math.floor(docWidth/50);
	 	} else {
	 		dimensionComponents = dimensionComponents[Math.floor(dimensionComponents.length/2)];
		 	tileWidth = dimensionComponents.factor;
		 	maxCols = dimensionComponents.multiplicator;
	 	}
	}


	/**
	 * Handler for window resize events
	 *
	 *
	 */
	function handleWindowResize(){
		//iterate over all windows and adjust their size based on their proportion of the screen
		var oldMaxCols = maxCols, oldMaxHeight = maxHeight;
		calcMaxSize();
 		boardSetup(maxCols, maxHeight);

 		for(var i = 0; i < tiles.length; i++){
 			var curTile = $('#'+tiles[i]);
 			var layout = layoutFix({
 				tileName: tiles[i],
 				x: parseInt(curTile.attr('col')),
 				y: parseInt(curTile.attr('row')),
 				sizex: parseInt(curTile.attr('sizex')),
 				sizey: parseInt(curTile.attr('sizey'))
 			})
 			curTile.attr({
 				'col':layout.y,
 				'row':layout.x,
 				'sizex':layout.sizex,
 				'sizey':layout.sizey
 			});
 			curTile.css({
 				'top':(layout.y - 1)*tileHeight + $('.tile-board').offset().top,
 				'left':(layout.x - 1)*tileWidth + $('.tile-board').offset().left,
 				'width':layout.sizex*tileWidth,
 				'height':layout.sizey*tileHeight
 			});
 			update_board(tiles[i]);
 		}
 		$('.tile-board').height(maxHeight * tileHeight);
 		$('.wrapper').height(maxHeight * tileHeight);
	}

	function checkZero(val){
		if(val == 0)
			return 1
		else
			return val
	}

	function boardSetup(cols, height){
		//i = cols, j = rows
		board = new Array(cols+1);
		//setup the empty board
		for (var i = board.length - 1; i >= 0; i--) {
			board[i] = new Array(height+1);
			for (var j = board[i].length - 1; j >= 0; j--) {
				board[i][j] = {
					occupied: 0,
					tile: ''
				};
			}
		}
	}


 	function factor( a ) {
		var c, i = 2, j = Math.floor( a / 2 ), output = [];
		for( ; i<=a; i++ ) {
			if(i == 1)
				return;
			c = a / i;
			if(c == 1)
				continue;
			if( c===Math.floor( c ) ) {
				var b = {
						'factor':c,
						'multiplicator':i
						};
				output.push(b);
  			}
 		}
 		return output;
 	}


 	function needsFixX(){
 		if(needsFixXBool){
 			return fixValX - 1;
 		} else {
 			return 0;
 		}
 	}

 	function needsFixY(){
 		if(needsFixYBool){
 			return fixValY - 1;
 		} else {
 			return 0;
 		}
 	}

});















