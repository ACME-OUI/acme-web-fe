self.addEventListener('message', (event) => {
	var url = event.data.url;
	var params = event.data.params;
	var method = event.data.method;
	var headers = event.data.headers;
	var resolve = (message) => {
		self.postMessage(JSON.stringify({
			'resolve': message
		}));
	}
	var reject = (message) => {
		self.postMessage(JSON.stringify({
			'reject': message
		}));
	}

	var xhr = new XMLHttpRequest();
	xhr.open(method, url);
	xhr.onload = () => {
		if(this.status == 200){
			resolve(xhr.response);
		} else {
			reject({
				status: this.status,
				statusText: this.statusText
			});
		}
	}
    xhr.onerror = function () {
      reject({
        status: this.status,
        statusText: xhr.statusText
      });
    };
    if (headers) {
      Object.keys(headers).forEach(function (key) {
        xhr.setRequestHeader(key, headers[key]);
      });
    }
    // We'll need to stringify if we've been given an object
    // If we have a string, this is skipped.
    if (params && typeof params === 'object') {
      params = Object.keys(params).map(function (key) {
        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
      }).join('&');
    }
    xhr.send(params);
    this.close();
});