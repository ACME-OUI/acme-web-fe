var cdms = {
	NDBuffer: function(buff, shape){
		this.buffer = buff;
		this.shape = shape;
		this.getVal = function() {
			value_ind = this.shapedIndicesToIndex.apply(this, arguments);
			return this.buffer[value_ind];
		};
		this.indexToShapedIndices = function(i) {
				var ind = 0;
				var shape_indices = [];
				for (ind = 0; ind < this.shape.length; ind++) {
					shape_indices.push(i / this.shape[ind]);
					i = i % this.shape[ind];
				}
				return shape_indices;
		};
		this.shapedIndicesToIndex = function() {
			var axis_ind = 0;
			if (arguments.length < this.shape.length) {
				return null;
			}
			var value_ind = 0;
			var iterind = 0;
			var multi_val;
			for (axis_ind = 0; axis_ind < this.shape.length; axis_ind++) {
				multi_val = 1;
				for (iterind = axis_ind + 1; iterind < this.shape.length; iterind++) {
					multi_val *= this.shape[iterind];
				}
				value_ind += multi_val * arguments[axis_ind];
			}
			return value_ind;
		}
		this.map = function(f) {
			var result_arr = [];
			for (var i = 0; i < this.buffer.length; i++) {
				result_arr.push(f(this.buffer[i], i, this));
			}
			return result_arr;
		};
	},
	getArray: function(url) {
		var promise = new Promise(function(resolve, reject) {
			var xhr = new XMLHttpRequest();
			xhr.responseType = "arraybuffer"
			xhr.open("GET", url);
			xhr.onload = function(ev) {
				var buffer = xhr.response;
				var headers = xhr.getAllResponseHeaders().split("\r\n").reduce(function(prev, cur) {
					var key, value;
					var parts = cur.split(": ");
					key = parts[0];
					value = parts[1];
					prev[key] = value;
					return prev;
				}, {});
				var dtype = headers["X-Cdms-Datatype"];
				switch (dtype) {
					case "float32":
						buffer = new Float32Array(buffer);
						break;
					case "float64":
						buffer = new Float64Array(buffer);
						break;
					case "int32":
						buffer = new Int32Array(buffer);
						break;
					case "int64":
						buffer = new Int64Array(buffer);
						break
					default:
						buffer = new Int32Array(buffer);
				}
				if (headers["X-Cdms-Shape"] !== undefined) {
					var shape = headers["X-Cdms-Shape"].replace('(', '');
					shape = shape.replace(')', '');
					shape = shape.split(",");
					shape = shape.map(function(d) { return parseInt(d); });
					buffer = new cdms.NDBuffer(buffer, shape);
				}
				resolve(buffer);
			}

			xhr.onerror = function(ev) {
				reject(Error("Unable to retrieve array from " + url));
			}
			xhr.send(null);
		});
		return promise;
	},
	open: function(file, run_name) {
		return new cdms.File(file, run_name);
	},
	Variable: function(file, id, run_name) {
		var url = "/cdat/nc_data?file=" + file + "&variable=" + id + "&run_name=" + run_name
		
		this.data = cdms.getArray(url);

		url = "/cdat/nc_meta?file=" + file + "&variable=" + id + "&run_name=" + run_name
		
		this.bounds = cdms.getArray(url);
	},
	File: function(file, run_name) {
		this.variables = new Promise(function(resolve, reject) {
			var xhr = new XMLHttpRequest();
			xhr.open("GET", "/cdat/get_file?file=" + file + '&run_name=' + run_name);

			xhr.onload = function(ev) {
				resolve(JSON.parse(xhr.responseText)["variables"]);
			}
			xhr.onerror = function(ev) {
				reject(Error("Unable to retrieve file info."));
			}
			xhr.send(null);
		});
		this.getVariable = function(var_id) {
			return this.variables.then(function(vars) {
				if (vars[1].indexOf(var_id) !== -1) {
					return new cdms.Variable(file, var_id, run_name);
				}
				return null;
			});
		}
	}
}
