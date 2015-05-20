/*
 * url = 
 * type = POST or GET
 * jsonStr = json object
 */
function get_data(url, type, jsonStr){
  var jsonObj = new Object;
  jsonObj.result = '';
  jsonObj.data = '';

  $.ajax({
    type: type,
    url: url,
    data: {user:jsonStr},
    dataType: 'json',
    success: function(data){
      jsonObj.result = 'success';
      jsonObj.data = data;
    }
    error: function(request, status, error){
      jsonObj.result = 'error';
      var errorObj = new Object;
      errorObj.request = request;
      errorObj.status = status;
      errorObj.error = error;
      var errorStr = JSON.stringify(errorObj);
      jsonObj.data = errorStr;

    }
  });

  var jsonStr = JSON.stringify(jsonObj);
  return jsonStr;
}

