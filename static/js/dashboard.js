$(function() {


	/****************************************
	 	Setup variables

	 	These could probably all be put in a resource file somewhere
	 ***************************************/

	// call the vis server setup
	cdat.setup()
		.then(function() {
				console.log('Vis instance launched');
			},
			function() {
				console.log(arguments);
			});


	var docHeight, docWidth, maxCols, maxHeight, tileHeight, tileWidth;
	var widthScale = .75; //represents the portion of the window allocated to tiles. Side bar is currently 25%
	var sidebarWidth = ($(window).width() * (1 - widthScale));
	calcMaxSize();
	$('#slide-menu-left').css('width', sidebarWidth);
	$('.wrapper').height(maxHeight * tileHeight);
	$('.wrapper').css({
    	"width": ($(window).width() * widthScale),
    	"float": "right"
    });
	$('.tile-board').css({
		'height': maxHeight * tileHeight
	});
	var tiles = [];
	var imgInstance = 0;
	var instance = 0; //variable that increments for every codemirror launched.
	var resize_handle_html = '<span class="gs-resize-handle gs-resize-handle-both"></span>';
	// Define a widget
	var header3 = '';
	var contents = '';
	var optionContents = '';
	var header1 = ['<div class="tile-panel panel-default">',
		' <div class="tile-panel-heading">',
		'  <div class="panel-header-title text-center">',
		'    <button type="button" class="btn btn-default btn-xs options" style="float:left;">',
		'     <span class="fa fa-cog" aria-label="Options"></span>',
		'    </button>',
		'    <button type="button" class="btn btn-default btn-xs remove"  style="float:right;">',
		'     <span class="fa fa-times" aria-label="Close"></span>',
		'    </button>',
		'     <p style="text-align: center">'
	].join('');
	// Widget Name
	header2 = ['     <p>',
		'   </div>',
		'  </div>',
		' </div>',
		' <div class="tile-panel-body" data-direction="horizontal" data-mode="slid">',
		'  <div class="tile-contents">'
	].join('');
	// Widget Contents
	content = '<div class="content"></div>';
	header3 += ' </div></div></div>';

	var altheader1 = ['<div class="tile-panel panel-default">',
		' <div class="tile-panel-heading">',
		'  <div class="panel-header-title text-center">',
		'     <p style="text-align: center">'
	].join('');

	var velo_context_menu_html = ['<div id="velo_context_menu">',
		'  <a href="#" id="velo_context_menu_delete">Delete</a>',
		'  <a href="#" id="velo_context_menu_rename">Rename</a>',
		'</div>'
	].join('');
	var esgf_context_menu_html = ['<div id="esgf_context_menu">',
		'  <a href="#" id="esgf_context_menu_search">Search</a>',
		'</div>'
	].join('');

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
	var opts = {
		lines: 17, // The number of lines to draw
		length: 40, // The length of each line
		width: 10, // The line thickness
		radius: 30, // The radius of the inner circle
		corners: 1, // Corner roundness (0..1)
		rotate: 0, // The rotation offset
		direction: 1, // 1: clockwise, -1: counterclockwise
		color: '#000', // #rgb or #rrggbb or array of colors
		speed: 1, // Rounds per second
		trail: 100, // Afterglow percentage
		shadow: false, // Whether to render a shadow
		hwaccel: false, // Whether to use hardware acceleration
		className: 'spinner', // The CSS class to assign to the spinner
		zIndex: 2e9, // The z-index (defaults to 2000000000)
		top: '50%', // Top position relative to parent
		left: '50%' // Left position relative to parent
	};
	var esgf_search_terms = {};
	var esgf_search_nodes = [];

	/****************************************
	 	End setup variables
	 	***************************************/

	//find if the user has a default layout, if so load it
	function loadDefaultLayout() {
		var jsonObj = new Object;
		jsonObj.result = '';
		jsonObj.data = '';

		get_data('load_layout/', 'GET', jsonObj, function(request) {
			var found_default = false;
			$.each(request, function(k, v) {
				if (v.default == true) {
					found_default = true;
					getFixVal(v.layout);
					loadLayout(v.layout, v.mode);
				}
			});
			if (!found_default) {
				fixValY = 0;
				fixValX = 0;
				mode = 'day';
			}
		}, function(request) {
			fixValY = 0;
			fixValX = 0;
			mode = 'day';
		});
	}

	function getFixVal(layouts) {
		if (layouts.length == 0) {
			fixValY = 0;
			fixValX = 0;
			mode = 'day';
			return;
		}
		for (var i = 0; i < layouts.length; i++) {
			layouts[i] = layoutFix(layouts[i]);
			if (layouts[i].x == 1) {
				needsFixXBool = false;
			} else {
				if (layouts[i].x < fixValX) {
					fixValX = layouts[i].x;
				}
			}
			if (layouts[i].y == 1) {
				needsFixYBool = false;
			} else {
				if (layouts[i].y < fixValY) {
					fixValY = layouts[i].y;
				}
			}
		}
	}


	/**
	 * A temporary function to deal with some aweful rounding issues
	 * Hopefully I will solve the problem and I can get rid of this :(
	 */
	function windowLoadFix() {
		var needsFixup = true;
		var alltiles = $('.tile');
		$('.tile').each(function() {
			if (parseInt($(this).attr('col')) == 1) {
				needsFixup == false;
			}
		});
		if (needsFixup) {
			$('.tile').each(function() {
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
	$('.slide-btn').each(function() {
		$(this).click(function() {
			var name = $(this).attr('id');
			var content = '';
			switch (name) {
				case 'cdat':
					content = '<div id="cdat-vis"></div>';

					// for example
					var view = cdat.show({
						file: 'http://test.opendap.org/opendap/hyrax/data/nc/coads_climatology.nc.nc4?',
						variable: 'SST',
						node: '#cdat-vis'
					}).then(
						function() {
							console.log('cdat vis success');
							// bind resize handler
							$('#cdat-vis').on('resizestop', view.render);

							// also need to bind `view.close` to some event triggered when the window closes
						},
						function() {
							console.log(arguments);
						}
					);

					break;

				default:
					{

					}
			}
			console.log( $('#' + name + '_window') )
			if ($('#' + name + '_window').length == 0) {
				var new_tile = '<li id="' + name + '_window" class="tile">' + header1 + name + header2 + content + header3 + '</li>';

				add_tile(new_tile, name + '_window', {
					ignore: 'true'
				}, function() {
					$('#search-btn').click(function() {
						nodeSearch(document.getElementById("node-search-name").value);
					});
				});
			}
		});
	});


	$(document).ready(function() {
		check_credentials('velo', function(code) {
			if (code == 200) {
				setup_velo();
			} else {
				content = ['<form id="velo_login">',
					'<h2 class="form-signin-heading">Please Sign In</h2>',
					'<label for="velo_username" class="sr-only">User name:</label>',
					'<input type="text" id="velo_username" name="velo_username" class="form-control" placeholder="User Name">',
					'<label for="velo_password" class="sr-only">Password:</label>',
					'<input type="password" id="velo_password" name="velo_password" class="form-control" placeholder="Password">',
					'<a id="submit_velo_user" class="btn btn-success" href="javascript:void(0);">Submit</a>'
				].join('');
				var new_tile = '<li id="velo_window" class="side-window">' + altheader1 + 'velo' + header2 + content + header3 + '</li>';
				add_sidebar_window(new_tile, 'velo_window', {
					ignore: 'true'
				}, function() {
					$('#search-btn').click(function() {
						nodeSearch(document.getElementById("node-search-name").value);
					});
				});
				$('#submit_velo_user').click(function() {
					var data = {};
					var cred = {
						'username': document.getElementById('velo_username').value,
						'password': document.getElementById('velo_password').value
					};
					data['velo'] = cred;
					get_data(
						'add_credentials/',
						'POST',
						data,
						function() {
							$('#velo_window').remove();
							removeHelper($('#' + 'velo_window'));
							setup_velo();
						},
						function() {
							alert('failed to save credentials');
						});
				});
			}
		});

		return;
	})


	function setup_velo() {
		content = ['<div id="velo-file-tree">',
			'   <div id="velo-options-bar">',
			'       <button class="fa fa-floppy-o velo-button" id="velo-options-bar-save" title="Save"></button>',
			'       <button class="fa fa-file-text-o velo-button" id="velo-options-bar-new-file" title="New File"></button>',
			'       <button class="fa fa-folder-o velo-button" id="velo-options-bar-new-folder" title="New Folder"></button>',
			'       <button class="fa fa-play-circle velo-button" id="velo-options-bar-start-run" title="Start Run"></button>',
			'       <button class="fa fa-refresh velo-button" id="velo-options-bar-refresh" title="Refresh"></button>',
			'   </div>',
			'   <div id="velo-mtree-container">',
			'	    <ul class="mtree" id="velo-mtree">',
			'	    </ul>',
			'   </div>',
			'</div>'
		].join('');
		name = 'Velo';
		var new_window = '<li id="velo_window" class="side-window">' + altheader1 + name + header2 + content + header3 + '</li>';
		add_sidebar_window(new_window, 'velo_window', {
			ignore: 'true'
		}, function() {
			$('#search-btn').click(function() {
				nodeSearch(document.getElementById("node-search-name").value);
			});
		});
		initFileTree('velo_window');
		var background = '';
		if (mode == 'day') {
			background = 'rgb(192, 192, 192)';
		} else {
			background = 'rgb(1, 1, 1)';
		}
		$('#velo-options-bar').find(':button').css({
			'background-color': background
		});
		$('#velo-options-bar-save').click(function() {
			velo_save_file();
		});
		$('#velo-options-bar-new-file').click(function() {
			velo_new_file();
		});
		$('#velo-options-bar-new-folder').click(function() {
			velo_new_folder();
		});
		$('#velo-options-bar-start-run').click(function() {
			velo_start_run();
		});
		$('#velo-options-bar-refresh').click(function() {
			velo_refresh();
		});
		load_layout();
	}

	$(document).ready(function() {
		content = '<div id="esgf-node-tree"></div>';
		name = 'esgf';
		initFileTree('esgf_window');
		var new_tile = '<li id="' + name + '_window" class="side-window">' + altheader1 + name + header2 + content + header3 + '</li>';
		add_sidebar_window(new_tile, name + '_window', {
			ignore: 'true'
		}, function() {
			$('#search-btn').click(function() {
				nodeSearch(document.getElementById("node-search-name").value);
			});
		});
	})

	//setup the hander to fix the windows after a resize
	$(window).resize(function() {
		if (event.target == this) {
			if (this.resizeTO) clearTimeout(this.resizeTO);
			this.resizeTO = setTimeout(function() {
				$(this).trigger('resizeEnd');
			}, 500);
		}

	});

	$(window).bind('resizeEnd', function() {
		//handleWindowResize();
	});

	$('.node-item').click(function() {
		if ($('#nodeSelect_window').length != 0) {
			$('#nodeSelect_window').find('.tile-contents').empty();
		} else {
			var new_tile = '<li id="' + "nodeSelect" + '_window" class="tile">' + header1 + "nodeSelect" + header2 + header3 + '</li>';
			add_tile(new_tile, "nodeSelect_window");

			$('#side-menu').append(html);
			var w = $('#' + id);
			$(w).css({
				'z-index': 1,
				'opacity': 0
			});
			console.log('setting options button id to ' + id + '_window_options');
			$(w).find('.fa-cog').parent().attr({
				id: id + '_options'
			});
			$(w).find('.fa-times').parent().attr({
				id: id + '_close'
			});

			$(w).find('.options').click(function(e) {

			});


		}
		var nodeName = $(this).find('a').text();
		populateNodeSelect(nodeName);

	});

	function velo_editor_save_file(event) {
		console.log("Editor save event fired.");
		console.log("Instance id : " + event.data.id);
		console.log(event.data.codeMirror.getValue());
		if ($('#velo-mtree [data-editor="' + event.data.id + '"]').length > 0) {
			var file_to_save = $('#velo-mtree [data-editor="' + event.data.id + '"]');
			console.log(file_to_save);
			var filename = file_to_save.text();
			var remote_path = file_to_save.attr('data-path');
			console.log("logging remote path:");
			console.log(remote_path);
			var text = event.data.codeMirror.getValue();
			var outgoing_request = {
				text: text,
				remote_path: remote_path,
				filename: filename
			}
			console.log(outgoing_request);
			get_data('velo_save_file/', 'POST', outgoing_request, function() {
				alert('file saved!');
				$(file_to_save).removeClass('mtree-unsaved');
			}, function() {
				alert('failed to save file');
			});
		};
	}
	function velo_save_file() {
		if ($('.mtree-active').length > 0) {
			$.getScript("static/js/spin.js", function() {
				if (mode == 'night') {
					var color = '#fff';
				} else {
					color = '#000';
				}
				opts.color = color;
				var spinner = new Spinner(opts).spin();
				//document.getElementById('velo-text-edit').appendChild(spinner.el);

				var file_to_save = $('#velo-mtree .mtree-active .mtree-unsaved');
				console.log(file_to_save);
				var filename = file_to_save.text();
				var remote_path = file_to_save.attr('data-path');
				console.log("logging remote path:");
				console.log(remote_path);

				var text = codeMirror.getValue();
				var outgoing_request = {
					text: text,
					remote_path: remote_path,
					filename: filename
				}
				console.log(outgoing_request);
				get_data('velo_save_file/', 'POST', outgoing_request, function() {
					spinner.stop();
					alert('file saved!');
					$('#velo-mtree .mtree-active .mtree-unsaved').removeClass('mtree-unsaved');
				}, function() {
					spinner.stop();
					alert('failed to save file');
				});
			});
		}
	}

	function velo_new_file() {
		var newFileHtml = ['<li id="velo-new-file-text-input-list">',
			'    <form id="velo-new-file-text-input-form">',
			'    	<input type="text" placeholder="New File Name" id="velo-new-file-text-input"></input>',
			'    </form>',
			'</li>'
		].join('');
		$('#velo-mtree .mtree-active ul').prepend(newFileHtml);
		$("#velo-new-file-text-input").keypress(function(event) {
			if (event.which == 13) {
				newFileHtml = '<a href="#" id="velo-new-file"></a>';
				var newFileName = document.getElementById('velo-new-file-text-input').value;
				if (isFolder(newFileName)) {
					newFileName += '.txt';
				}
				$('#velo-new-file-text-input-form').remove();
				$('#velo-new-file-text-input-list').append(newFileHtml);
				$('#velo-new-file').text(newFileName);
				$('#velo-new-file').addClass('velo-file');
				$('#velo-mtree.mtree-active').removeClass('mtree-active');
				$('#velo-new-file-text-input-list').addClass('mtree-active');
				var path = $('#velo-new-file').parent().parent().attr('data-path') + '/' + newFileName;
				$('#velo-new-file').attr({
					'data-path': path,
					'id': ''
				});
				console.log("creating path:");
				console.log(path);
				var text = '';
				var outgoing_request = {
					text: text,
					remote_path: path,
					filename: newFileName
				}
				//Saving new files since other actions will cause the tree to be refreshed.
				//If they are not saved, refreshing the file tree will remove new files. 
				console.log(outgoing_request);
				get_data('velo_save_file/', 'POST', outgoing_request, function() {
					alert('file saved!');
				}, function() {
					alert('failed to save file');
				});
				$('a[data-path="' + path + '"]').click(function(e) {
					var path = $(e.target).attr('data-path');
					var id = 'dashboard_tile_' + instance;
					var content = '<div class="content"></div>';
					var new_tile = '<li id="' + id + '" class="tile" data-path="' + path + '" > ' + header1 + path + header2 + content + header3 + '</li>';
					add_tile(new_tile, id , {ignore: 'true'}, initCodeMirror('', id, path));
				});
			}
		});
	}

	function velo_new_folder() {
		var newFolderHtml = ['<li id="velo-new-folder-text-input-list">',
			'    <form id="velo-new-folder-text-input-form">',
			'    	<input type="text" placeholder="New Folder Name" id="velo-new-folder-text-input"></input>',
			'    </form>',
			'</li>'
		].join('');
		$('#velo-mtree .mtree-active ul').prepend(newFolderHtml);
		$("#velo-new-folder-text-input").keypress(function(event) {
			if (event.which == 13) {
				newFolderHtml = '<a href="#" id="new-velo-folder"></a><ul class="mtree-level-2" style="overflow: hidden; height: 0px; display: none;"></ul>';
				var newFolderName = document.getElementById('velo-new-folder-text-input').value;
				$('#velo-new-folder-text-input-form').remove();
				$('#velo-new-folder-text-input-list').addClass('mtree-node mtree-closed');
				$('#velo-new-folder-text-input-list').append(newFolderHtml);

				$('#new-velo-folder').text(newFolderName);
				// Set mtree-active class on list items for last opened element
				$('.mtree li > *:first-child').on('click.mtree-active', function(e) {
					if ($(this).parent().hasClass('mtree-closed')) {
						$('.mtree-active').not($(this).parent()).removeClass('mtree-active');
						$(this).parent().addClass('mtree-active');
					} else if ($(this).parent().hasClass('mtree-open')) {
						$(this).parent().removeClass('mtree-active');
					} else {
						$('.mtree-active').not($(this).parent()).removeClass('mtree-active');
						$(this).parent().toggleClass('mtree-active');
					}
				});

				$('#velo-mtree .mtree').bind('contextmenu', function(e) {
					e.preventDefault();
					if (e.button == 2) {
						velo_context_menu(e);
					}
				});

				get_data('velo_new_folder/', 'POST', {
					'foldername': newFolderName
				}, function(response) {
					alert('Success creating new folder');
				}, function(response) {
					alert('Error when creating new folder');
				})
			}
		});

	}

	function velo_start_run() {
		data = {
			user: $("#velo_window .mtree-root a").html(),
			runspec: $("#velo_window .mtree-active a").data("path"),
		}
		//data = JSON.stringify(data);
		get_data('../poller/', 'POST', data
				, function(response) {
					alert('Success creating new run');
				}, function(response) {
					alert('Error when creating new run');
				})
	}

	function velo_refresh() {
		id = 'velo_window';
		$('#velo-mtree').empty();
		initFileTree(id);
	}

	function esgf_context_menu(e) {
		$('body').append(esgf_context_menu_html);
		$('#esgf_context_menu').offset({
			'top': e.clientY,
			'left': e.clientX
		});
		createMask('esgf_context_menu', 0);
		$('#esgf_context_menu_search').click(function(e) {
			//$('#esgf_window .tile-contents').empty();
			fadeOutMask('esgf_context_menu');
			var target = $('#esgf-mtree .mtree-active ul').attr('data-node');
			nodeSearch(target);
		});
	}

	function velo_context_menu(e) {
		$.getScript("static/js/spin.js", function() {
			if (mode == 'night') {
				var color = '#fff';
			} else {
				color = '#000';
			}
			opts.color = color;

			var name = $(e.target).siblings().attr('data-path');
			if (typeof name === 'undefined') {
				name = $(e.target).attr('data-path');
			}
			$('body').append(velo_context_menu_html);
			$('#velo_context_menu').offset({
				'top': e.clientY,
				'left': e.clientX
			});
			$('#velo_context_menu_delete').attr({
				'data-name': name
			});
			$('#velo_context_menu_rename').attr({
				'data-name': name
			});
			createMask('velo_context_menu', 0);
			$('#velo_context_menu_delete').click(function(e) {
				var spinner = new Spinner(opts).spin();
				document.getElementById('velo-file-tree').appendChild(spinner.el);
				data = {
					'name': $('#velo_context_menu_delete').attr('data-name')
				};
				get_data('velo_delete/', 'POST', data, function(response) {
					spinner.stop();
					var target = $('ul[data-path="' + JSON.parse(data)['name'] + '"]');
					if (target.length == 0) {
						target = $('a[data-path="' + JSON.parse(data)['name'] + '"]');
					}
					target.parent().fadeOut().queue(function() {
						target.parent().remove();
					});
				}, function(response) {
					spinner.stop();
					alert('delete failure');
				});
				fadeOutMask('velo_context_menu');
			});
			$('#velo_context_menu_rename').click(function(e) {
				var spinner = new Spinner(opts).spin();
				document.getElementById('velo-file-tree').appendChild(spinner.el);

				fadeOutMask('velo_context_menu');
			});
		});
	}

	function initCodeMirror(text, id, path) {
		console.log("Instance var = " + instance);
		var saveId = '"velo-editor-save-' + instance + '"';
		content = '<div id="velo-text-edit-' + instance + '"><button class="fa fa-floppy-o velo-button" id=' + saveId + ' title="Save"></button></div>';
		$('#' + id + ' .content').append(content);
		$('#velo-text-edit-'+instance).on("click", {instance:instance}, function(event) {
			$('#velo-mtree .mtree-active').removeClass('mtree-active');
			console.log()
			$('#velo-mtree [data-editor="' + event.data.instance + '"]').parent('li').addClass('mtree-active');
		});
		$.getScript("static/js/codemirror.js", function() {
			if (mode == 'night') {
				var theme = 'twilight';
			} else {
				theme = '3024-day';
			}
			codeMirror = CodeMirror(document.getElementById('velo-text-edit-' + instance), {
				'theme': theme,
				'dragDrop': false,
				'lineNumbers': true,
				'showCursorWhenSelecting': true,
				'mode': 'text/python'
			});
			$('#velo-editor-save-' + instance).on("click", {id:instance, codeMirror:codeMirror}, function(event){ //store instance into event.data.id
				velo_editor_save_file(event);
			});
			$('a[data-path="' + path + '"]').attr('data-editor', instance);
			codeMirror.setValue(text);
			codeMirror.on('change', function(event) {
				codeMirrorTextChanged(event);
			});
		});
	}


	function codeMirrorTextChanged(event, i) {
		var elem = $('#velo-mtree .mtree-active > a')
		if($(elem[1]).length > 0){
			$(elem[1]).addClass('mtree-unsaved');
		}
		else {
			$(elem[0]).addClass('mtree-unsaved');
		}
	}



	function getFile(url, id) {
		$.getScript("static/js/spin.js", function() {
			if (mode == 'night') {
				var color = '#fff';
			} else {
				color = '#000';
			}
			opts.color = color;
			var spinner = new Spinner(opts).spin();
			//document.getElementById('velo-text-edit').appendChild(spinner.el);
			var path = url.split('/');
			filename = path.pop();
			var path = path.join('/');
			data = {
				'filename': filename,
				'path': path
			}
			get_data('get_file/', 'POST', data, function(response) {
				spinner.stop();
				$('#velo-text-edit').empty();
				if (response.type == 'image') {
					// var name = 'Image Viewer: ' + id;
					// var windowId = 'image_viewer_' + imgInstance;
					var contents = '<div id="velo-image"><img src="/acme/userdata/image/' + response.location + '"></div>'
					// var new_tile = '<li id="' + windowId + '_window" class="tile" data-path="' + id + '">' + header1 + name + header2 + contents + header3 + '</li>';
					// add_tile(new_tile, windowId + '_window', {ignore: 'true'});	
					// imgInstance++;
					$('#' + id + ' .content').append(contents);
				}
				else {
				initCodeMirror(response.responseText, id, url);
				}
			}, function(response) {
				spinner.stop();
				alert('Failed to retrieve file from server');
			});
		});
	}

	function initFileTree(window_id) {

		$.getScript("static/js/spin.js", function() {
			if (mode == 'night') {
				var color = '#fff';
			} else {
				color = '#000';
			}
			opts.color = color;
			var spinner = new Spinner(opts).spin();
			if (mode == 'day') {
				$('#velo-file-tree').css({
					'background-color': '#FAFFFF'
				});
				$('#esgf-node-tree').css({
					'background-color': '#FAFFFF'
				});
				$('#velo-text-edit').css({
					'background-color': '#f7f7f7'
				});
			} else {
				$('#velo-file-tree').css({
					'background-color': '#111'
				});
				$('#esgf-node-tree').css({
					'background-color': '#111'
				});
				$('#velo-text-edit').css({
					'background-color': '#141414'
				});
			}
			if (window_id == 'velo_window') {
				document.getElementById('velo_window').appendChild(spinner.el);
				/*
					The server adds the CURRENT_USER/velo_credentials to the end of the folder request
				*/
				request = {
					'file': '/User Documents/'
				}

				get_data('get_folder/', 'POST', request, function(response) {
					spinner.stop();
					response.sort();
					for (var i = 0; i < response.length; i++) {
						if (response[i] == '/User Documents/' || response[i] == 'Velo Initialized...') {
							response.splice(i, 1);
							i--;
							continue;
						}
						var path = response[i].split('/');
						var name = path[path.length - 1];
						if (isFolder(response[i])) {
							var parentFolder = '/';
							for (j = 1; j < path.length - 1; j++) {
								parentFolder += path[j] + '/';
							}
							parentFolder = parentFolder.substring(0, parentFolder.length - 1);
							var parentFolderEl = $('ul[data-path="' + parentFolder + '"]');
							if (parentFolderEl.length == 0) {
								$('#velo-mtree.mtree').append('<li class="mtree-root"><a href="#">' + path[path.length - 1] + '</a><ul data-path="' + response[i] + '"></ul></li>');
								continue;
							}
							var folderPath = parentFolder + '/' + path[path.length - 1];
							var folderName = path[path.length - 1];
							parentFolderEl.append('<li class="mtree-drag mtree-drop"><a href="#">' + folderName + '</a><ul data-path="' + folderPath + '"></ul></li>');

						} else {
							parentFolder = '/';
							for (j = 1; j < path.length - 1; j++) {
								parentFolder += path[j] + '/';
							}
							parentFolder = parentFolder.substring(0, parentFolder.length - 1);
							$('ul[data-path="' + parentFolder + '"]').append('<li class="mtree-drag mtree-file"><a href="#" data-path="' + response[i] + '">' + path[path.length - 1] + '</a></li>');
							$('a[data-path="' + response[i] + '"]').addClass('velo-file');
							$('a[data-path="' + response[i] + '"]').click(function(event) {

								console.log($(event.target).attr('data-path'));
								var id = 'dashboard_tile_' + instance;
								var path = $(event.target).attr('data-path');
								content = '<div class="content"></div>';
								var new_tile = '<li id="' + id + '" class="tile" data-path="' + path + '" > ' + header1 + path + header2 + content + header3 + '</li>';
								add_tile(new_tile, id , { ignore: 'true'}, getFile(path, id)); 
							}); //this is totally not doing what i thought it would, but it works. Pretty sure that getFile
						}       //is getting called instead of being passed as a callback. 
					}

					mtree('velo-mtree-container');

					$('#velo-mtree.mtree').bind('contextmenu', function(e) {
						e.preventDefault();
						if (e.button == 2) {
							velo_context_menu(e);
						}
					});
					$('.mtree-drag').draggable({
						revert: 'invalid',
						stack: '#velo-mtree-container',
					});
					// $('.mtree-drag-and-sort').sortable({
					// 	revert: 'true',
					// 	placeholder: "ui-state-highlight",
					// 	stop: function(){
					// 		mtree('velo-mtree-container')
					// 	}
					// });
					//$('.mtree-drag-and-sort').disableSelection();
					$('.mtree-drop').droppable({
						drop: function(event, ui) {
							console.log(event);
							console.log(ui);

						}
					});
				}, function() {
					spinner.stop();
					alert('error getting home folder');
				});
			} else if (window_id == 'esgf_window') {
				document.getElementById('esgf_window').appendChild(spinner.el);
				get_data('node_info/', 'GET', {}, function(response) {
					spinner.stop();
					$('#esgf-node-tree').append('<ul class="mtree" id="esgf-mtree"></ul>');
					var node_array = Object.keys(response);
					var length = node_array.length;
					if (length > 10) {
						length = 10
					}
					for (var i = 0; i < length; i++) {

						var node_attrib = Object.keys(response[node_array[i]]['attributes']);
						//var node_child = Object.keys(response[node_array[i]]['children']);
						var node_child = 'Node';
						if (response[node_array[i]]['children'][node_child]) {
							var host = response[node_array[i]]['children'][node_child]['attributes']['hostname'];
							$('#esgf-mtree').append('<li><a href="#">' + node_array[i] + '</a><ul data-node="' + host + '"></li>');
							$('ul[data-node="' + host + '"]').append('<input type="checkbox" class="node-check-box" value="' + host + '">Search Node</input>');
							for (var j = 0; j < node_attrib.length; j++) {
								var attribute;
								var children;
								if (node_attrib[j] == 'timeStamp') {
									var d = new Date(0);
									d.setUTCSeconds(response[node_array[i]]['attributes'][node_attrib[j]] / 1000);
									attribute = 'date node came online ' + d;
								} else {
									attribute = response[node_array[i]]['attributes'][node_attrib[j]];
								}
								children = Object.keys(response[node_array[i]]['children'][node_child]['attributes']);

								$('ul[data-node="' + host + '"]').append('<li><table><tr><td>' + node_attrib[j] + '</td><td style="text-align: right;"> ' + attribute + '</td></tr></table></li>');
							}
							for (var k = 0; k < children.length; k++) {
								if (children[k] == 'timeStamp') {
									var d = new Date(0);
									d.setUTCSeconds(response[node_array[i]]['children'][node_child]['attributes'][children[k]] / 1000);
									attribute = 'node online at ' + d;
								} else {
									attribute = response[node_array[i]]['children'][node_child]['attributes'][children[k]];
								}
								$('ul[data-node="' + host + '"]').append('<li><table><tr><td>' + children[k] + '</td><td style="text-align: right;">' + attribute + '</td></tr></table></li>');
							}
						}
					}
					$('#esgf-mtree.mtree').bind('contextmenu', function(e) {
						e.preventDefault();
						if (e.button == 2) {
							esgf_context_menu(e);
						}
					});
					mtree('esgf-node-tree');
				}, function(response) {
					alert('Error getting node list');
					spinner.stop();
				});
			}
		});
	}



	function isFolder(file) {
		if (file.split('.').pop() != file) {
			return false;
		} else {
			return true;
		}
	}

	function populateFile(file) {
		alert(file);
	}

	/* Checks with the server to see if the users has credentials for 
	 *  the requested service in the servers database
	 *
	 * service_name -> the name of the service to check credentials for
	 */
	function check_credentials(service_name, cb) {
		var data = {
			'service': service_name
		};
		var exists = false;
		var done = false;
		var csrftoken = get_csrf();

		$.ajax({
			url: 'credential_check_existance/',
			data: JSON.stringify(data),
			type: 'POST',
			dataType: 'json',
			statusCode: {
				200: function(response) {
					cb(response.status);
				},
				500: function(response) {
					cb(response.status);
				}
			},
			headers: {
				"X-CSRFToken": csrftoken
			}
		});

		return exists;
	}


	/* Creates the window for searching a node for its data
	 *
	 * hostname -> the hostname of the node to search
	 *
	 */
	function nodeSearch(hostname) {
		$.getScript("static/js/spin.js", function() {
			if (mode == 'night') {
				var color = '#fff';
			} else {
				color = '#000';
			}
			opts.color = color;
			var spinner = new Spinner(opts).spin();


			//get  facets
			var nodes_to_search = [];
			$.each($('.node-check-box:checked'), function(box, value) {
				nodes_to_search.push($(value).val());
			});
			esgf_search_nodes = nodes_to_search;
			$('#esgf_window #esgf-node-tree').remove();
			document.getElementById('esgf_window').appendChild(spinner.el);
			get_data('load_facets/', 'POST', nodes_to_search, function(response) {
				spinner.stop();
				var newHtml = '<div id="esgf-node-search"><ul class="mtree" id="esgf-node-search-mtree"></ul></div>';
				$('#esgf_window .tile-contents').append(newHtml);
				newHtml = '<div><input type="text" id="esgf-search-terms" placeholder="Type search terms here or select options below"></input></div>';
				$('#esgf_window .tile-contents').prepend(newHtml);
				newHtml = '<button class="btn btn-primary" id="esgf-search-submit">Search</button>';
				$('#esgf_window .tile-contents').prepend(newHtml);
				var keys = Object.keys(response).sort();

				for (var i = 0; i < keys.length; i++) {
					var facet = response[keys[i]];
					var facet_html = '<li><a href="#">' + keys[i] + '</a><ul data-facet="' + keys[i] + '" class="facet"></ul></li>';
					$('#esgf-node-search-mtree').append(facet_html);
					var facet_options = Object.keys(response[keys[i]]).sort();
					for (var j = 0; j < facet_options.length; j++) {
						var facet_options_html = '<li><table><tr><td><a href="#">' + facet_options[j] + '</a></td><td style="text-align: right;">' + response[keys[i]][facet_options[j]] + '</td></tr></table></li>';
						$('ul[data-facet="' + keys[i] + '"').append(facet_options_html);
					}
					$('ul[data-facet="' + keys[i] + '"]').click(function(e) {
						esgf_search_terms[$(e.target).parents('.facet').attr('data-facet')] = $(e.target).text();
						var terms = Object.keys(esgf_search_terms);
						var terms_string = '';
						for (var i = 0; i < terms.length; i++) {
							terms_string += terms[i] + '=' + esgf_search_terms[terms[i]] + ',';
						}
						terms_string = terms_string.substring(0, terms_string.length - 1);
						document.getElementById('esgf-search-terms').value = terms_string;
					});
				}
				mtree('esgf-node-search');
				$('#esgf-search-submit').click(function() {
					var terms = document.getElementById('esgf-search-terms').value.split(/[=,]+/);
					esgf_search_terms = {};
					for (var i = 0; i < terms.length - 1; i += 2) {
						esgf_search_terms[terms[i]] = terms[i + 1];
					}
					esgfSearch();
				});
			}, function() {
				spinner.stop();
				alert('Failed to load node facets');
			});
		});
	}

	function esgfSearch() {
		$.getScript("static/js/spin.js", function() {
			if (mode == 'night') {
				var color = '#fff';
			} else {
				color = '#000';
			}
			opts.color = color;
			var spinner = new Spinner(opts).spin();
			document.getElementById('esgf_window').appendChild(spinner.el);
			data = {
				'nodes': esgf_search_nodes,
				'terms': esgf_search_terms
			}

			function display_response(r, parent, hitnum) {
				keys = Object.keys(r).sort();
				var branch = '';

				for (var i = 0; i < keys.length; i++) {
					if (typeof r[keys[i]] != 'object') {
						branch = '<li><table><tr><td>' + keys[i] + '</td><td style="float:right;"> ' + r[keys[i]] + '</td></tr></table></li>';
						parent.append(branch);
					} else {
						branch = '<li><a href="#">' + keys[i] + '</a><ul data-branch="' + hitnum + keys[i] + '"></ul></li>';
						parent.append(branch);
						var subkeys = Object.keys(r[keys[i]]);
						for (var j = 0; j < subkeys.length; j++) {
							branch = '<li><table><tr><td>' + subkeys[j] + '</td><td style="float:right;"> ' + r[keys[i]][subkeys[j]] + '</td></tr></table></li>';
							$('ul[data-branch="' + hitnum + keys[i] + '"]').append(branch);
						}
					}
				}
			}


			get_data('node_search/', 'POST', data, function(response) {
				spinner.stop();

				var searchDisplay = '<div id="esgf-search-display"><ul class="mtree" id="esgf-search-display-mtree"></ul></div>';
				if ($('#esgf-search-display').length == 0) {
					$('#esgf_window .tile-contents').append(searchDisplay);
				} else {
					$('#esgf-search-display').empty();
					$('#esgf_window .tile-contents').append(searchDisplay);
				}
				for (var i in response) {
					if (i != 'hits') {
						$('#esgf-search-display-mtree').append('<li><a href="#">Dataset: ' + (parseInt(i) + 1) + '</a><ul data-branch="' + i + '"></ul></li>');
						display_response(response[i], $('ul[data-branch="' + i + '"]'), i);
					}
				}
				$('#esgf-search-display-mtree').offset({
					'top': $('#esgf-node-search').offset.top,
					'left': $('#esgf-node-search').offset.left + $('#esgf-node-search').width()
				});
				mtree('esgf-search-display');
			}, function() {
				spinner.stop();
				alert('No data found, ease search restrictions and try again');
			});
		});
	}


	/**
	 * Adds a given window to the sidebar.
	 * Based off the add tile function, but with the tile system removed. 
	 **/

	function add_sidebar_window(html, id) {
		var w = $('#' + id);
		$(w).replaceWith(html);
		console.log(id);
		$(w).css({
			'z-index': 1,
			'opacity': 1
		});
		return $(w);
	};


	/**
	 * Creates a new tile window and rearranges all the other tiles to make room
	 * html-> the content of the tile
	 * id-> the name for the new tile to take
	 * options-> whatever new options i decided to add, right now a x,y,sizex,sizey to handle window sizes
	 * callback-> an optional function to pass that will be called with add_tile is done
	 */
	function add_tile(html, id, options, callback) {
		$('.tile-holder').append(html);
		var w = $('#' + id);
		$(w).css({
			'z-index': 1,
			'opacity': 0
		});
		console.log('setting options button id to ' + id + '_window_options');
		$(w).find('.fa-cog').parent().attr({
			id: id + '_options'
		});
		$(w).find('.fa-times').parent().attr({
			id: id + '_close'
		});

		$(w).draggable({
			//containment: '.tile-board',
			helper: 'clone',
			start: function(event, ui) {
				ui.helper.find('.tile-contents').hide();
				ui.helper.addClass('ui-draggable-dragging-no-transition');
				ui.helper.animate({
					'opacity': '0.5',
					'z-index': 10,
					'width': '20%',
					'height': '20%',
				});
			},
			stop: function(event, ui) {
				ui.helper.find('.tile-contents').show();
				var pos = grid_from_offset(ui.position);
				dragFixup(pos.col, pos.row);
				$(ui.helper).css({
					'opacity': '1.0',
					'z-index': 1,
				});
			},
			cursorAt: {
				left: 200,
				top: 15
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
			start: function(event, ui) {
				handleResizeStart(event, ui);
			},
			resize: function(event, ui) {
				event.stopPropagation();
			},
			stop: function(event, ui) {
				handleResizeStop(event, ui);
				event.stopPropagation();
			}
		});

		$(w).find('.ui-resizable-n').mousedown(function() {
			resizeDir = 'n';
		});
		$(w).find('.ui-resizable-s').mousedown(function() {
			resizeDir = 's';
		});
		$(w).find('.ui-resizable-e').mousedown(function() {
			resizeDir = 'e';
		});
		$(w).find('.ui-resizable-w').mousedown(function() {
			resizeDir = 'w';
		});

		tiles.push($(w).attr('id'));

		//Setup the live tile for the options menu
		$(w).find('.live-tile').liveTile({
			direction: 'horizontal'
		});

		//Stop the body from being able to drag
		$(w).find('.tile-panel-body').mousedown(function(event) {
			event.stopPropagation();
		});

		$(w).find('.tile-panel-heading').mousedown(function(event) {
			dragStartId = w[0].id;
			var grid = $('#' + dragStartId);
			dragStartX = parseInt(grid.attr('col'));
			dragStartY = parseInt(grid.attr('row'));
			dragStartSizeX = parseInt(grid.attr('sizex'));
			dragStartSizeY = parseInt(grid.attr('sizey'));
			dragStartOffset = grid.offset();
		});

		$(w).find('.remove').click(function(e) {

			$('#' + id).remove();
			for (var i = tiles.length - 1; i >= 0; i--) {
				if (tiles[i] == id) {
					tiles.splice(i, 1);
					break;
				}
			};
			positionFixup();
		});

		$(w).find('.options').click(function(e) {

		});

		if (options != null && options.ignore != 'true') {
			$(w).attr({
				'row': options.y,
				'col': options.x,
				'sizex': options.sizex,
				'sizey': options.sizey
			});
			update_board(id);
			var tile_offset = offset_from_location(parseInt($(w).attr('row')), parseInt($(w).attr('col')));
			$(w).css({
				"top": tile_offset.top,
				"left": tile_offset.left,
				"width": $(w).attr('sizex') * tileWidth,
				"height": $(w).attr('sizey') * tileHeight
			});
			console.log(tileWidth);
			console.log(tileHeight);
			console.log(options.sizex);
			console.log(options.sizey);
		} else {
			positionFixup();
		}
		if ($('body').attr('class') == 'night') {
			$(w).find('.tile-panel-body').css({
				'background-color': '#0C1021;',
				'border-color': '#00f;',
				'color': '#fff'
			});
		}
		$(w).animate({
			'opacity': 1
		}, 'slow', 'easeOutCubic');

		if (callback != null) {
			callback();
		}
		instance++;
		return $(w);
	};

	/**
	 * Handles all actions at the start of a resize event
	 * event -> The event variable
	 * ui -> the ui element handed down from the jquery handler
	 */
	function handleResizeStart(event, ui) {
		resizeStartX = parseInt(ui.element.attr('col'));
		resizeStartSizeX = parseInt(ui.element.attr('sizex'));
		resizeStartY = parseInt(ui.element.attr('row'));
		resizeStartSizeY = parseInt(ui.element.attr('sizey'));
		switch (resizeDir) {
			case 'n':
				$('#' + ui.element.attr('id')).css({
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
	function handleResizeStop(event, ui) {
		resizeFixup(ui);
		var el = ui.element;
		el.css({
			'left': (parseInt(el.attr('col')) - 1) * tileWidth + $('.tile-holder').offset().left,
			'height': parseInt(el.attr('sizey')) * tileHeight,
			'width': parseInt(el.attr('sizex')) * tileWidth
		});
		setTimeout(function(el) {
			if (resizeDir == 'n' && parseInt(el.attr('row')) == 1) {
				el.css({
					'top': $('.tile-board').offset().top,
					'height': tileHeight * parseInt(el.attr('sizey')),
					'width': tileWidth * parseInt(el.attr('sizex'))
				});
			} else if (resizeDir == 's') {
				el.css({
					'height': tileHeight * parseInt(el.attr('sizey')),
					'width': tileWidth * parseInt(el.attr('sizex'))
				});
			} else if (resizeDir == 'e' && parseInt(el.attr('col')) + parseInt(el.attr('sizex')) - 1 == maxCols) {
				el.css({
					'left': tileWidth * (parseInt(el.attr('col')) - 1) + $('.tile-holder').offset().left,
					'width': tileWidth * parseInt(el.attr('sizex')),
					'height': tileWidth * parseInt(el.attr('sizey'))
				});

			} else if (resizeDir == 'w' && parseInt(el.attr('col')) == 1) {
				el.css({
					'width': tileWidth * parseInt(el.attr('sizex')),
					'height': tileWidth * parseInt(el.attr('sizey')),
					'left': $('.tile-board').offset().left
				});
			} else {
				el.css({
					'left': (parseInt(el.attr('col')) - 1) * tileWidth + $('.tile-holder').offset().left,
					'height': parseInt(el.attr('sizey')) * tileHeight,
					'width': parseInt(el.attr('sizex')) * tileWidth
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

	function recursiveResize(moved, dir, diff, side, id) {
		var curWindow = $('#' + id);
		var x = parseInt(curWindow.attr('col'));
		var y = parseInt(curWindow.attr('row'));
		var sizex = parseInt(curWindow.attr('sizex'));
		var sizey = parseInt(curWindow.attr('sizey'));
		var toAdd = true;
		var adj = new Array();
		if (dir == 'up') {
			if (side == 'n') {
				//var adj = new Set();
				for (var i = x; i < x + sizex; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[i - 1][y - 2].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[i - 1][y - 2].tile);
					}
				};
				var helperReturn = adjHelper(adj, moved);
				var startY = curWindow.offset().top;
				curWindow.attr({
					'row': y - diff,
					'sizey': sizey + diff
				});
				curWindow.css({
					//'top':(y-diff)*tileHeight + $('.navbar').height() - 1,
					'top': startY - (diff * tileHeight),
					'height': (sizey + diff) * tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, done resizing
					return;
				} else {
					//we need to keep resizing
					recursiveResize(moved, dir, diff, 's', helperReturn.adj[0]);
				}
			} else if (side == 's') {
				for (var i = x; i < x + sizex; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[i - 1][y + sizey - 1].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[i - 1][y + sizey - 1].tile);
					}
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizey': sizey - diff
				});
				curWindow.css({
					'height': (sizey - diff) * tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, all windows have been resized
					return;
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'n', helperReturn.adj[0]);
				}
			} else {
				//error
				return
			}
		} else if (dir == 'down') {
			if (side == 'n') {
				for (var i = x; i < x + sizex; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[i - 1][y - 2].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[i - 1][y - 2].tile);
					}
				};
				//check the base case-> all windows have been moved
				moved.add(id);
				var helperReturn = adjHelper(adj, moved);
				var startY = curWindow.offset().top;
				curWindow.attr({
					'row': y - diff,
					'sizey': sizey + diff
				});
				curWindow.css({
					//'top':(y-diff)*tileHeight + $('.navbar').height() - 1,
					'top': startY - (diff * tileHeight),
					'height': (sizey + diff) * tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, done resizing
					return;
				} else {
					//we need to keep resizing
					recursiveResize(moved, dir, diff, 's', helperReturn.adj[0]);
				}
			} else if (side == 's') {
				for (var i = x; i < x + sizex; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[i - 1][y + sizey - 1].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[i - 1][y + sizey - 1].tile);
					}
				};
				//check the base case-> all windows have been moved
				moved.add(id);
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizey': sizey - diff
				});
				curWindow.css({
					'height': (sizey - diff) * tileHeight
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished == true) {
					//base case, all windows have been resized
					return;
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'n', helperReturn.adj[0]);
				}
			} else {
				//error
				return
			}
		} else if (dir == 'right') {
			if (side == 'e') {
				for (var i = y; i < y + sizey; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[x + sizex - 1][i - 1].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[x + sizex - 1][i - 1].tile);
					}
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizex': sizex - diff
				});
				curWindow.css({
					'width': (sizex - diff) * tileWidth,
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, all windows have been resized
					return;
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'w', helperReturn.adj[0]);
				}
			} else if (side == 'w') {
				for (var i = y; i < y + sizey; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[x - 2][i - 1].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[x - 2][i - 1].tile);
					}
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'col': x - diff,
					'sizex': sizex + diff
				});
				curWindow.css({
					'width': (sizex + diff) * tileWidth,
					'left': (x - diff - 1) * tileWidth + $('.tile-holder').offset().left
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, all windows have been resized
					return;
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'e', helperReturn.adj[0]);
				}
			} else {
				//error
				return
			}
		} else if (dir == 'left') {
			if (side == 'e') {
				for (var i = y; i < y + sizey; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[x + sizex - 1][i - 1].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[x + sizex - 1][i - 1].tile);
					}
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'sizex': sizex - diff
				});
				curWindow.css({
					'width': (sizex - diff) * tileWidth,
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, all windows have been resized
					return;
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'w', helperReturn.adj[0]);
				}
			} else if (side == 'w') {
				for (var i = y; i < y + sizey; i++) {
					for (var j = 0; j < adj.length; j++) {
						if (adj[j] == board[x - 2][i - 1].tile) {
							toAdd = false;
							break;
						} else {
							toAdd = true;
						}
					}
					if (toAdd) {
						adj.push(board[x - 2][i - 1].tile);
					}
				};
				var helperReturn = adjHelper(adj, moved);
				curWindow.attr({
					'col': x - diff,
					'sizex': sizex + diff
				});
				curWindow.css({
					'width': (sizex + diff) * tileWidth,
					'left': (x - diff - 1) * tileWidth + $('.wrapper').offset().left
				});
				update_board(id);
				moved.add(id);
				removeHelper(curWindow);
				if (helperReturn.finished) {
					//base case, all windows have been resized
					return;
				} else {
					//we need to keep resizeing 
					recursiveResize(moved, dir, diff, 'e', helperReturn.adj[0]);
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
		adj.forEach(function(item) {
			if (!moved.has(item)) {
				done = false;
			} else {
				adj.splice(adj.indexOf(item), 1);
			}
		}, moved);

		return {
			'finished': done,
			'adj': adj
		};
	}


	/**
	 * Helper to handle removing an occluded tile from the list of tiles
	 * tile -> the tile to check if it should be removed
	 */
	function removeHelper(tile) {
		if (parseInt(tile.attr('sizex')) <= 0 || parseInt(tile.attr('sizey')) <= 0) {
			$.when(tile.fadeOut()).then(function() {
				tile.remove();
			});
			for (var i = tiles.length - 1; i >= 0; i--) {
				if (tiles[i] == tile.attr('id')) {
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
	function resizeFixup(ui) {
		var resizeId = ui.element.attr('id');
		//which direction did it resize?
		if (resizeDir == 'n') {
			var diff = virtical_location(ui.originalPosition.top, 0) - virtical_location(ui.helper.position().top, 0);
			if (diff <= 0 && parseInt(ui.element.attr('row')) <= 1) {
				//the tile is at the top
				return;
			}
			var virt_adj = new Set();
			for (var i = resizeStartX; i < resizeStartX + resizeStartSizeX; i++) {
				if (board[i - 1][resizeStartY - 2].tile != resizeId) {
					virt_adj.add(board[i - 1][resizeStartY - 2].tile);
				}
			};
			//did it go up or down?
			$(ui.element).attr({
				'row': parseInt(ui.element.attr('row')) - diff,
				'sizey': parseInt(ui.element.attr('sizey')) + diff
			});
			update_board(resizeId);
			var moved = new Set();
			moved.add(resizeId);
			if (diff < 0) {
				//it moved down
				virt_adj.forEach(function(item) {
					recursiveResize(moved, 'down', diff, 's', item);
				});
			} else if (diff > 0) {
				//it moved up
				virt_adj.forEach(function(item) {
					recursiveResize(moved, 'up', diff, 's', item);
				});
			}
		}
		if (resizeDir == 's') {
			var diff = virtical_location(ui.originalPosition.top, ui.originalSize.height) - virtical_location(ui.helper.position().top, ui.helper.height());
			if (parseInt(ui.element.attr('row')) + parseInt(ui.element.attr('sizey')) - 1 == maxHeight) {
				//the tile is at the bottom
				return;
			}
			var virt_adj = new Set();
			for (var i = resizeStartX; i < resizeStartX + resizeStartSizeX; i++) {
				if (board[i - 1][resizeStartY + resizeStartSizeY - 1].tile != resizeId) {
					virt_adj.add(board[i - 1][resizeStartY + resizeStartSizeY - 1].tile);
				}
			};
			//did it go up or down?
			$(ui.element).attr({
				'sizey': parseInt(ui.element.attr('sizey')) - diff
			});
			update_board(resizeId);
			var moved = new Set();
			moved.add(resizeId);
			if (diff < 0) {
				//it moved down
				virt_adj.forEach(function(item) {
					recursiveResize(moved, 'down', diff, 'n', item);
				});
			} else if (diff > 0) {
				//it moved up
				virt_adj.forEach(function(item) {
					recursiveResize(moved, 'up', diff, 'n', item);
				});
			}
		}
		if (resizeDir == 'e') {
			if (parseInt(ui.element.attr('col')) + parseInt(ui.element.attr('sizex')) - 1 == maxCols) {
				//the element is on the right of the board
				return;
			}
			var horz_adj = new Set();
			for (var i = resizeStartY; i < resizeStartY + resizeStartSizeY; i++) {
				if (board[resizeStartX + resizeStartSizeX - 1][i - 1].tile != resizeId) {
					horz_adj.add(board[resizeStartX + resizeStartSizeX - 1][i - 1].tile);
				}
			};
			//did it go right or left?
			var diff = horizontal_location(ui.originalPosition.left, ui.originalSize.width) - horizontal_location(ui.helper.position().left, ui.helper.width());
			ui.element.attr({
				'sizex': parseInt(ui.element.attr('sizex')) - diff
			});
			update_board(resizeId);
			var moved = new Set();
			moved.add(resizeId);
			if (diff < 0) {
				//it moved right
				horz_adj.forEach(function(item) {
					recursiveResize(moved, 'right', diff, 'w', item);
				});
			} else if (diff > 0) {
				//it moved left
				horz_adj.forEach(function(item) {
					recursiveResize(moved, 'left', diff, 'w', item);
				});
			}
		}
		if (resizeDir == 'w') {
			if (parseInt(ui.element.attr('col')) == 1) {
				//the element is on the left side of the board
				return;
			}
			var horz_adj = new Set();
			for (var i = resizeStartY; i < resizeStartY + resizeStartSizeY; i++) {
				if (board[resizeStartX - 2][i - 1].tile != resizeId) {
					horz_adj.add(board[resizeStartX - 2][i - 1].tile);
				}
			};
			//did it go right or left?
			var diff = horizontal_location(ui.originalPosition.left, 0) - horizontal_location(ui.helper.position().left, 0);
			ui.element.attr({
				'col': parseInt(ui.element.attr('col')) - diff,
				'sizex': parseInt(ui.element.attr('sizex')) + diff
			});
			update_board(resizeId);
			var moved = new Set();
			moved.add(resizeId);
			if (diff < 0) {
				//it moved right

				horz_adj.forEach(function(item) {
					recursiveResize(moved, 'right', diff, 'e', item);
				});
			} else if (diff > 0) {
				//it moved left
				horz_adj.forEach(function(item) {
					recursiveResize(moved, 'left', diff, 'e', item);
				});
			}
		}
	}

	/**
	 * Fixes the positions for all windows
	 */
	function positionFixup() {
		for (var i = tiles.length - 1; i >= 0; i--) {
			var layout = returnBalanced(maxCols, maxHeight);
			var t = $('#' + tiles[i]);
			t.attr({
				'row': layout[tiles.length - 1][i].row(maxHeight),
				'col': layout[tiles.length - 1][i].col(maxCols),
				'sizex': layout[tiles.length - 1][i].sizex(maxCols),
				'sizey': layout[tiles.length - 1][i].sizey(maxHeight)
			});
			var tile_offset = offset_from_location(parseInt(t.attr('row')), parseInt(t.attr('col'))); 
			t.css({
				"top": tile_offset.top,
				"left": tile_offset.left,
				"width": t.attr('sizex') * tileWidth * widthScale,
				"height": t.attr('sizey') * tileHeight
			});

			console.log( tile_offset.top );
			console.log( tile_offset.left );
			console.log( t.attr('sizex') * tileWidth);
			console.log( t.attr('sizey') * tileHeight );
			update_board(tiles[i]);
		};
	}


	/**
	 * Updates the board to match the tile
	 * id -> the id of the tile to update the board info for
	 */
	function update_board(id) {
		var t = $('#' + id);
		for (var k = parseInt(t.attr('col')) - 1; k < parseInt(t.attr('col')) + parseInt(t.attr('sizex')) - 1; k++) {
			for (var j = parseInt(t.attr('row')) - 1; j < parseInt(t.attr('row')) + parseInt(t.attr('sizey')) - 1; j++) {
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
	function offset_from_location(row, col) {
		var offset = $('.tile-board').offset();
		offset.left += (col - 1) * tileWidth; //account for other tiles
		offset.top += (row - 1) * tileHeight;
		offset.left = ((offset.left - sidebarWidth) * widthScale) + sidebarWidth; //reduce widths to the portion of the screen not used by the sidebar
		return offset;
	}

	/**
	 * Fixes the window positions after a drag event
	 * col, row -> the ending col and row of the dragged element
	 */
	function dragFixup(col, row) {

		if (col < 0 || col > maxCols || row < 0 || row > maxHeight) {
			$('.ui-draggable-dragging').remove();
			return;
		}
		var targetId = board[col - 1][row - 1].tile;
		var targetX = parseInt($('#' + targetId).attr('col'));
		var targetY = parseInt($('#' + targetId).attr('row'));
		var targetSizeX = parseInt($('#' + targetId).attr('sizex'));
		var targetSizeY = parseInt($('#' + targetId).attr('sizey'));
		var targetGrid = $('#' + targetId);
		var startGrid = $('#' + dragStartId);
		if (targetId == dragStartId) {
			var targetOffset = offset_from_location(row, col);
			$('#' + targetId).css({
				'top': dragStartOffset.top,
				'left': dragStartOffset.left,
				'height': dragStartSizeY * tileHeight,
				'width': dragStartSizeX * tileWidth
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
				'top': targetOffset.top,
				'left': targetOffset.left,
				'width': parseInt(startGrid.attr('sizex')) * tileWidth * widthScale,
				'height': parseInt(startGrid.attr('sizey')) * tileHeight
			});
			update_board(dragStartId);

			targetGrid.attr({
				'col': dragStartX,
				'row': dragStartY,
				'sizex': dragStartSizeX,
				'sizey': dragStartSizeY
			});
			targetGrid.css({
				'top': dragStartOffset.top,
				'left': dragStartOffset.left,
				'width': parseInt(targetGrid.attr('sizex')) * tileWidth * widthScale,
				'height': parseInt(targetGrid.attr('sizey')) * tileHeight
			});
			update_board(targetId);
		}
	}


	/**
	 * Returns the row and col of an element from its offset
	 * pos -> the position of the object
	 */
	function grid_from_offset(pos) {
		var location = {
			col: Math.floor(pos.left / tileWidth) + 1,
			row: Math.floor(pos.top / tileHeight) + 1
		}
		return location;
	}

	/**
	 * Returns the col from the position and size of an element
	 * x -> the horizontal position of the object
	 * sizex -> the horizontal size of the object
	 */
	function horizontal_location(x, sizex) {
		if (((x + sizex) / tileWidth) % 1 >= 0.5) {
			return Math.ceil((x + sizex) / tileWidth) + 1;
		} else {
			return Math.floor((x + sizex) / tileWidth) + 1;
		}
	}

	/**
	 * Returns the row from the position and size of an element
	 * y -> the horizontal position of the object
	 * sizey -> the horizontal size of the object
	 */
	function virtical_location(y, sizey) {
		if (((y + sizey) / tileHeight) % 1 >= 0.5) {
			return Math.ceil((y + sizey) / tileHeight) + 1
		} else {
			return Math.floor((y + sizey) / tileHeight) + 1;
		}
	}


	/***********************************
	Left slide menu
	***********************************/
	var body = document.body;

	// function leftMenuToggle() {
	// 	$('#slide-menu-left').toggle('slide', {
	// 		direction: 'left',
	// 		easing: 'easeOutCubic'
	// 	}, 500);
	// 	if ($('#toggle-left-a').text() == 'Open Menu') {
	// 		$('#toggle-left-a').text('Close Menu');
	// 	} else {
	// 		$('#toggle-left-a').text('Open Menu');
	// 	}
	// }

	// $('#toggle-slide-left').click(function(e) {
	// 	leftMenuToggle();
	// });

	// window.onbeforeunload =	function save_layout() { //TODO: make this use ajax instead of local storage
	// 	var pathsToSave = [];
	// 	if(typeof(Storage) !== "undefined") {
	//     	$('.tile-holder .tile').each( function (index, element) {
	//     		pathsToSave.push($(element).attr('data-path'));
	// 		});
	// 		localStorage.setItem("pathsToLoad", JSON.stringify(pathsToSave));
	// 		console.log(JSON.parse(localStorage.getItem("pathsToLoad")));
	// 	}
	// 	 else {
	// 		console.log('Unable to save layout. Browser does not support local storage.')
	// 	}
	// }


	$('#save-layout').click(function() {
	//	save_layout();
	//	leftMenuToggle();
	// 	createMask('save-menu');

	// 	var saveMenu = document.createElement('div');
	// 	$(saveMenu).addClass('bvc');
	// 	$(saveMenu).addClass('save-layout');
	// 	$(saveMenu).attr({
	// 		'id': 'save-menu'
	// 	});
	// 	var saveMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
	// 	saveMenuHtml += '<form name="save-layout-form" id="save-form">';
	// 	saveMenuHtml += 'Layout Name:<br><input type="text" id="layout-name">';
	// 	saveMenuHtml += '<input type="submit" value="Save" id="save-btn"><br>';
	// 	saveMenuHtml += '<input type="checkbox" name="default" value="default" id="default">Default Layout';
	// 	saveMenuHtml += '</form></div><div class="bevel bl br"></div>';
	// 	$(saveMenu).html(saveMenuHtml);
	// 	$('body').append(saveMenu);
	 	$('#save-btn').click(function(event) {
	 		event.preventDefault();
	 		var layout_name = 'default';
	 		var layout = [];
			$('.tile').each(function() {
				layout.push({
					tileName: $(this).attr('id').substr(0, $(this).attr('id').indexOf('_')),
					tilePath: $(this).attr('data-path'),
					x: parseInt($(this).attr('col')) / maxCols,
					y: parseInt($(this).attr('row')) / maxHeight,
					sizex: parseInt($(this).attr('sizex')) / maxCols,
					sizey: parseInt($(this).attr('sizey')) / maxHeight
				});
			});
			if ($('body').hasClass('night')) {
				var mode = 'night';
			} else {
				mode = 'day'
			}
			var data = {
				instance: instance,
				name: layout_name,
				mode: mode,
				style: 'balanced',
				layout: layout,
				default_layout: document.getElementById('default').checked
			};

	 		get_data('save_layout/', 'POST', data, function() {
	 			alert('Layout saved');
	 		}, function() {
	 			alert('Please use a unique layout name');
	 		});
	// 		fadeOutMask('save-menu');
	 	});
	});


	// $('#load-layout').click(function() {
	// 	var options = {};
	// 	get_data('load_layout/', 'GET', new Object(), function(request) {
			//parse response
			
			// createMask('load-layout-menu');

			// //create load menu and populate with values
			// var loadMenu = document.createElement('div');
			// $(loadMenu).addClass('bvc');
			// $(loadMenu).addClass('save-layout');
			// $(loadMenu).attr({
			// 	'id': 'load-layout-menu'
			// });
			// var loadMenuHtml = '<div class="bevel tl tr"></div><div class="content">'
			// loadMenuHtml += '<form name="load-layout-form" id="save-form">';
			// loadMenuHtml += 'Select Layout:<br><select id="select-layout">';
			// $.each(options, function(k, v) {
			// 	loadMenuHtml += '<option value="' + v.name + '" id="layout-' + v.name + '">' + v.name + '</option>';
			// });
			// loadMenuHtml += '</select><input type="submit" value="Load" id="load-button">';
			// loadMenuHtml += '</form></div><div class="bevel bl br"></div>';
			// $(loadMenu).html(loadMenuHtml);
			// $('body').append(loadMenu);


			$('#load-layout').click(function() {
				//var name = document.forms['load-layout-form'].elements[0].options[document.forms['load-layout-form'].elements[0].selectedIndex].text;
				name ='default';
				var data = {
					'layout_name': name
				};
				get_data('load_layout/', 'POST', data, function(request) {
					//fadeOutMask('load-layout-menu');
					$('.tile').each(function() {
						$(this).remove();
					});
					options = request;
					tiles = [];
					layout = []
					$.each(request.board_layout, function(k, v) {
						layout.push(layoutFix(v));
					});
					loadLayout(layout, request.mode);
				}, function() {
					alert('failed to load layout');
					fadeOutMask('load-layout-menu');
				});
			});


	/**
	 * Resolves the size of the layout to match the current page
	 * layout -> the layout for one tile at a time
	 */
	function layoutFix(layout) {

		layout.x = checkZero(Math.round(layout.x * maxCols));
		layout.y = checkZero(Math.round(layout.y * maxHeight));
		layout.sizex = checkZero(Math.round(layout.sizex * maxCols));
		layout.sizey = checkZero(Math.round(layout.sizey * maxHeight));
		var diff = layout.x + layout.sizex - 1 - maxCols
		if (diff > 0) {
			layout.sizex -= diff;
		}
		diff = layout.y + layout.sizey - 1 - maxHeight;
		if (diff > 0) {
			layout.sizey -= diff;
		}
		return layout;
	}


	/**
	 * loads a layout onto the page
	 * layout -> a full layout with all the tiles
	 * mode -> the day/night mode of the layout
	 */
	function loadLayout(layout, mode) {
		fadeOutMask();
		if (mode == 'day') {
			setDay();
		} else if (mode == 'night') {
			setNight();
		}
		mode.light = mode

		for (var i = 0; i < layout.length; i++) {
			var name = layout[i].tileName;
			var new_tile = '<li id="' + name + '_window" class="tile">' + header1 + name + header2 + contents + header3 + '</li>';
			add_tile(new_tile, name + '_window', {
				x: layout[i].x - needsFixX(),
				y: layout[i].y - needsFixY(),
				sizex: layout[i].sizex,
				sizey: layout[i].sizey
			});
		}
	}

	function createMask(id, opacity) {
		var mask = document.createElement('div');
		$(mask).addClass('mask');
		$(mask).attr({
			'id': 'mask'
		});
		if (typeof opacity !== 'undefined') {
			$(mask).css({
				'opacity': opacity
			});
		}
		$(mask).click(function() {
			fadeOutMask(id);
		});
		$('body').append(mask);
		$(mask).fadeIn();
	}

	function fadeOutMask(id) {
		$('#' + id).remove();
		$('#mask').fadeOut('fast').queue(function() {
			$('#mask').remove();
		});
	}

	function setNight() {
		mode = 'night'
		$('body').attr({
			'class': 'night'
		});
		$('.tile-panel-body').each(function() {
			$(this).css({
				'background-color': '#0C1021;',
				'border-color': '#00f;',
				'color': '#fff'
			});
		});
		$(body).attr({
			'background-color': '#051451!important',
			'color': '#aaa!important'
		});
		$('#dark-mode-toggle').text('Dark mode is on');
		//handle velo window
		if ($('#velo_window').length != 0) {
			$('.mtree').removeClass('jet');
			$('.mtree').addClass('transit');
			$('#velo-file-tree').css({
				'background-color': '#111'
			});
			$('#velo-text-edit').css({
				'background-color': '#141414'
			});
			if (typeof codeMirror !== 'undefined') {
				codeMirror.setOption('theme', 'twilight');
			}
		}
		$('#velo-options-bar').find(':button').css({
			'background-color': 'rgb(1, 1, 1)'
		});
	}

	function setDay() {
		mode = 'day'
		$('body').attr({
			'class': 'day'
		});
		$('.tile-panel-body').each(function() {
			$(this).css({
				'background-color': '#fff;',
				'color': '#111;',
				'border-color': '#000;'
			});
		});
		$(body).attr({
			'background-color': '#fff',
			'color': '#000'
		});
		$('#dark-mode-toggle').text('Dark mode is off');
		$('.mtree').removeClass('transit');
		$('.mtree').addClass('jet');
		//handle velo window
		if ($('#velo_window').length != 0) {
			$('#velo-file-tree').css({
				'background-color': '#FAFFFF'
			});
			$('#velo-text-edit').css({
				'background-color': '#f7f7f7'
			});
			if (typeof codeMirror !== 'undefined') {
				codeMirror.setOption('theme', '3024-day');
			}
		}
		$('#velo-options-bar').find(':button').css({
			'background-color': 'rgb(192, 192, 192)'
		});

	}


	$('#dark-mode-toggle').click(function(e) {
		if ($('body').attr('class') == 'day') {
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
	$('#drop-down-tab').click(function(e) {
		var menuHeight = parseInt($('#drop-down-menu').css('height'));
		$('.node-carousel').hide();
		setTimeout(function() {
			$('.node-carousel').slick({
				infinite: true,
				slidesToShow: 3,
				slidesToScroll: 1,
			});

		}, 50);
		$('.node-carousel').show();
		if ($('#drop-down-menu').css('display') == 'none') {
			$('.tile').each(function() {
				$(this).css({
					'top': parseInt($(this).css('top')) + menuHeight
				});
			});
		} else {
			$('.tile').each(function() {
				$(this).css({
					'top': parseInt($(this).css('top')) - menuHeight
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

	function calcMaxSize() {
		docHeight = $(window).height() - $('.navbar').height() - 10;
		docHeight -= docHeight % 10;
		docWidth = $(window).width();
		docWidth -= docWidth % 10;
		var dimensionComponents = factor(docHeight).sort(function(a, b) {
			return a.factor - b.factor
		});
		for (var i = 0; i < dimensionComponents.length; i++) {
			if (dimensionComponents[i].multiplicator % 10 != 0) {
				dimensionComponents.splice(i, 1);
				i--;
			}
		}
		if (dimensionComponents.legnth == 0) {
			tileHeight = 50;
			maxHeight = Math.floor(docHeight) / 50;
		} else {
			dimensionComponents = dimensionComponents[Math.floor(dimensionComponents.length / 2)];
			tileHeight = dimensionComponents.factor;
			maxHeight = dimensionComponents.multiplicator;
		}

		dimensionComponents = factor(docWidth).sort(function(a, b) {
			return a.factor - b.factor
		});
		for (var i = 0; i < dimensionComponents.length; i++) {
			if (dimensionComponents[i].multiplicator % 10 != 0) {
				dimensionComponents.splice(i, 1);
				i--;
			}
		}
		if (dimensionComponents.length == 0) {
			tileWidth = 50;
			maxCols = Math.floor(docWidth / 50);
		} else {
			dimensionComponents = dimensionComponents[Math.floor(dimensionComponents.length / 2)];
			tileWidth = dimensionComponents.factor; //uhhhhh hopefully this is right
			maxCols = dimensionComponents.multiplicator;
		}
	}


	/**
	 * Handler for window resize events
	 *
	 *
	 */
	function handleWindowResize() {
		//iterate over all windows and adjust their size based on their proportion of the screen
		var oldMaxCols = maxCols,
			oldMaxHeight = maxHeight;
		calcMaxSize();
		boardSetup(maxCols, maxHeight);

		for (var i = 0; i < tiles.length; i++) {
			var curTile = $('#' + tiles[i]);
			var layout = layoutFix({
				tileName: tiles[i],
				x: parseInt(curTile.attr('col')),
				y: parseInt(curTile.attr('row')),
				sizex: parseInt(curTile.attr('sizex')),
				sizey: parseInt(curTile.attr('sizey'))
			})
			curTile.attr({
				'col': layout.y,
				'row': layout.x,
				'sizex': layout.sizex,
				'sizey': layout.sizey
			});
			curTile.css({
				'top': (layout.y - 1) * tileHeight + $('.tile-board').offset().top,
				'left': (layout.x - 1) * tileWidth + $('.tile-board').offset().left,
				'width': layout.sizex * tileWidth,
				'height': layout.sizey * tileHeight
			});
			update_board(tiles[i]);
		}
		$('.tile-board').height(maxHeight * tileHeight);
		$('.wrapper').height(maxHeight * tileHeight);
	}

	function checkZero(val) {
		if (val == 0)
			return 1
		else
			return val
	}

	function boardSetup(cols, height) {
		//i = cols, j = rows
		board = new Array(cols + 1);
		//setup the empty board
		for (var i = board.length - 1; i >= 0; i--) {
			board[i] = new Array(height + 1);
			for (var j = board[i].length - 1; j >= 0; j--) {
				board[i][j] = {
					occupied: 0,
					tile: ''
				};
			}
		}
	}


	function factor(a) {
		var c, i = 2,
			j = Math.floor(a / 2),
			output = [];
		for (; i <= a; i++) {
			if (i == 1)
				return;
			c = a / i;
			if (c == 1)
				continue;
			if (c === Math.floor(c)) {
				var b = {
					'factor': c,
					'multiplicator': i
				};
				output.push(b);
			}
		}
		return output;
	}


	function needsFixX() {
		if (needsFixXBool) {
			return fixValX - 1;
		} else {
			return 0;
		}
	}

	function needsFixY() {
		if (needsFixYBool) {
			return fixValY - 1;
		} else {
			return 0;
		}
	}

	function get_csrf() {
		var nameEQ = "csrftoken=";
		var ca = document.cookie.split(';');
		for (var i = 0; i < ca.length; i++) {
			var c = ca[i];
			while (c.charAt(0) == ' ') c = c.substring(1, c.length);
			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
		}
		return null;
	}

	function get_data(url, type, jsonObj, success_callback, fail_callback) {
		var csrftoken = get_csrf();

		// var jsonObj = new Object;®
		// jsonObj.result = '';
		// jsonObj.data = '';
		data = JSON.stringify(jsonObj);
		var ajax_obj = $.ajax({
			type: type,
			url: url,
			data: data,
			dataType: 'json',
			success: function(data) {
				jsonObj.result = 'success';
				jsonObj.data = data;
				success_callback(jsonObj.data);
			},
			headers: {
				"X-CSRFToken": csrftoken
			},
			error: function(request, status, error) {
				jsonObj.result = 'error';
				if (request.status == 200) {
					success_callback(request);
					return;
				}
				var errorObj = new Object;
				errorObj.request = request;
				errorObj.status = status;
				errorObj.error = error;
				var errorStr = JSON.stringify(errorObj);
				jsonObj.data = errorStr;
				console.log(jsonObj);
				fail_callback(status);

			}
		});
		return ajax_obj;
	}


	function mtree(id) {
		if (typeof id === 'undefined') {
			id = 'tile-contents';
		}
		/*
		The following is copied from mtree.js
		*/
		// mtree.js
		// Only apply if mtree list exists
		if ($('#' + id + ' ul.mtree').length) {
			// Settings
			var collapsed = true; // Start with collapsed menu (only level 1 items visible)
			var close_same_level = true; // Close elements on same level when opening new node.
			var duration = 400; // Animation duration should be tweaked according to easing.
			var listAnim = true; // Animate separate list items on open/close element (velocity.js only).
			var easing = 'easeOutQuart'; // Velocity.js only, defaults to 'swing' with jquery animation.

			if (mode == 'day') {
				var mtree_style = 'jet';
			} else {
				mtree_style = 'transit';
			}
			$('.mtree').addClass(mtree_style);

			// Set initial styles 
			$('#' + id + ' .mtree ul').css({
				'overflow': 'hidden',
				'height': (collapsed) ? 0 : 'auto',
				'display': (collapsed) ? 'none' : 'block'
			});

			// Get node elements, and add classes for styling
			var node = $('#' + id + ' .mtree li:has(ul)');
			node.each(function(index, val) {
				$(this).children(':first-child').css('cursor', 'pointer')
				$(this).addClass('mtree-node mtree-' + ((collapsed) ? 'closed' : 'open'));
				$(this).children('ul').addClass('mtree-level-' + ($(this).parentsUntil($('#' + id + ' ul.mtree'), 'ul').length + 1));
			});

			// Set mtree-active class on list items for last opened element
			$('#' + id + ' .mtree li > *:first-child').on('click.mtree-active', function(e) {
				if ($(this).parent().hasClass('mtree-closed')) {
					$('.mtree-active').not($(this).parent()).removeClass('mtree-active');
					$(this).parent().addClass('mtree-active');
				} else if ($(this).parent().hasClass('mtree-open')) {
					$(this).parent().removeClass('mtree-active');
				} else {
					$('.mtree-active').not($(this).parent()).removeClass('mtree-active');
					$(this).parent().toggleClass('mtree-active');
				}
			});

			// Set node click elements, preferably <a> but node links can be <span> also
			node.children(':first-child').on('click.mtree', function(e) {

				// element vars
				var el = $(this).parent().children('ul').first();
				var isOpen = $(this).parent().hasClass('mtree-open');

				// close other elements on same level if opening 
				if ((close_same_level || $('.csl').hasClass('active')) && !isOpen) {
					var close_items = $(this).closest('ul').children('.mtree-open').not($(this).parent()).children('ul');

					// Velocity.js
					if ($.Velocity) {
						close_items.velocity({
							height: 0
						}, {
							duration: duration,
							easing: easing,
							display: 'none',
							delay: 100,
							complete: function() {
								setNodeClass($(this).parent(), true)
							}
						});

						// jQuery fallback
					} else {
						close_items.delay(100).slideToggle(duration, function() {
							setNodeClass($(this).parent(), true);
						});
					}
				}

				// force auto height of element so actual height can be extracted
				el.css({
					'height': 'auto'
				});

				// listAnim: animate child elements when opening
				if (!isOpen && $.Velocity && listAnim) el.find(' > li, li.mtree-open > ul > li').css({
					'opacity': 0
				}).velocity('stop').velocity('list');

				// Velocity.js animate element
				if ($.Velocity) {
					el.velocity('stop').velocity({
						//translateZ: 0, // optional hardware-acceleration is automatic on mobile
						height: isOpen ? [0, el.outerHeight()] : [el.outerHeight(), 0]
					}, {
						queue: false,
						duration: duration,
						easing: easing,
						display: isOpen ? 'none' : 'block',
						begin: setNodeClass($(this).parent(), isOpen),
						complete: function() {
							if (!isOpen) $(this).css('height', 'auto');
						}
					});

					// jQuery fallback animate element
				} else {
					setNodeClass($(this).parent(), isOpen);
					el.slideToggle(duration);
				}

				// We can't have nodes as links unfortunately
				e.preventDefault();
			});

			// Function for updating node class
			function setNodeClass(el, isOpen) {
				if (isOpen) {
					el.removeClass('mtree-open').addClass('mtree-closed');
				} else {
					el.removeClass('mtree-closed').addClass('mtree-open');
				}
			}

			// List animation sequence
			if ($.Velocity && listAnim) {
				$.Velocity.Sequences.list = function(element, options, index, size) {
					$.Velocity.animate(element, {
						opacity: [1, 0],
						translateY: [0, -(index + 1)]
					}, {
						delay: index * (duration / size / 2),
						duration: duration,
						easing: easing
					});
				};
			}

			// Fade in mtree after classes are added.
			// Useful if you have set collapsed = true or applied styles that change the structure so the menu doesn't jump between states after the function executes.
			if ($('#' + id + ' .mtree').css('opacity') == 0) {
				if ($.Velocity) {
					$('.mtree').css('opacity', 1).children().css('opacity', 0).velocity('list');
				} else {
					$('.mtree').show(200);
				}
			}
		}

		/*
			End mtree.js
		*/
	}

});