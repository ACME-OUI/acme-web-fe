(function(){
	if (!Array.prototype.last){
	    Array.prototype.last = function(){
	        return this[this.length - 1];
	    };
	};

  window.ACMEDashboard = window.ACMEDashboard || {};

  window.ACMEDashboard.isJson = function(str) {
      try {
          JSON.parse(str);
      } catch (e) {
          return false;
      }
      return true;
  }

	window.ACMEDashboard.ajax = function(data){
      var url = data.url;
      var params = data.params;
      var method = data.method;
      var headers = data.headers;
      console.log(data);

      var xhr = new XMLHttpRequest();
      xhr.open(method, url);
      if (headers) {
        Object.keys(headers).forEach(function (key) {
          xhr.setRequestHeader(key, headers[key]);
        });
      }
      // We'll need to stringify if we've been given an object
      // If we have a string, this is skipped.
      if(method == 'POST') {
      	params = JSON.stringify(params);
      }
      else if (params && typeof params === 'object') {
        params = Object.keys(params).map(function (key) {
          return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
        }).join('&');
      }
      console.log('sending params: ' + params);
      xhr.send(params);
      xhr.onreadystatechange = ensureReadiness;
    
      function ensureReadiness() {
        if(xhr.readyState < 4) {
          return;
        }
          
        if(xhr.status !== 200) {
          return;
        }

        // all is well  
        if(xhr.readyState === 4) {
          console.log('got a good reply')
          complete(xhr.responseText);
        }     
      }
    };
}).call(this);

