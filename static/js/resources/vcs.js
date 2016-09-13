var vcs = {
	init: function(el, server) {
		if(server){
			vcs.server = server;
		}
		return new vcs.Canvas(el);
	},
        getColormap: function(name) {
		var promise = new Promise(function(resolve, reject) {
			var xhr = new XMLHttpRequest();
			var url;
			if(vcs.server){
				url = vcs.server + "/vcs?type=colormap&name=" + name
			} else {
				url = "/vcs?type=colormap&name=" + name
			}
			xhr.open("GET", url);
			xhr.onload = function(ev) {
				resolve(JSON.parse(xhr.response));
			};
			xhr.send(null);
		});

		return  promise;
        },
	Canvas: function(el) {
		var conf = {
			"animation": false,
			"baseLayerPicker": false,
			"fullscreenButton": false,
			"geocoder": false,
			"homeButton": false,
			"infoBox": false,
			"sceneModePicker": true,
			"selectionIndicator": false,
			"timeline": false,
			"navigationHelpButton": false,
			"navigationInstructionsInitiallyVisible": false,
			"useDefaultRenderLoop": true,
			"showRenderLoopErrors": false,
			"automaticallyTrackDataSourceClocks": false,
			"orderIndependentTranslucency": false
		};
		this.viewer = new Cesium.Viewer(el, conf);
		this.boxfill = function(variable) {
			var viewer = this.viewer;
			return Promise.all([variable.bounds, variable.data, vcs.getColormap("default")]).then(function(results){
				var bounds = results[0];
				var data = results[1];
				var cmap = results[2];

				if (bounds.shape[0] != data.buffer.length) {
					console.log("Sizes don't match :(");
					return;
				}

				var max = Math.max.apply(null, data.buffer);
				var min = Math.min.apply(null, data.buffer);

				function color_for_val(val) {
					var spread = max - min;
					var pct = (val - min) / spread * 256;
					if (pct === 256) {
						pct = 255;
					}
					var colors = cmap.index.data[Math.floor(pct)];
					var red = colors[0];
					var green = colors[1];
					var blue = colors[2];
	 				return new Cesium.Color(red / 100, green / 100, blue / 100);
				}

				var entities = data.map(function(val, ind){
					var points = [];
					for (var i = 0; i < bounds.shape[1]; i++) {
						// Push lon then lat
						points.push(bounds.getVal(ind, i, 0));
						points.push(bounds.getVal(ind, i, 1));
					}
					return viewer.entities.add({
						name: "cell_" + ind,
						polygon: {
							hierarchy: Cesium.Cartesian3.fromDegreesArray(points),
							material: color_for_val(val).withAlpha(.5),
							outline: true,
							outlineColor: Cesium.Color.BLACK
						}
					});
				});

				return entities;
			});
		};
	}
}
