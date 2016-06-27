(function(){
  var dashboard = angular.module('dashboard', ['esgf', 'velo', 'cdat'])
  .controller('DashboardControl', ['$scope', '$http', function($scope, $http){


    $scope.init = function(){

    };

    $scope.add_window = function(window_name){
      
    }



    $scope.get_csrf = function() {
  		var nameEQ = "csrftoken=";
  		var ca = document.cookie.split(';');
  		for (var i = 0; i < ca.length; i++) {
  			var c = ca[i];
  			while (c.charAt(0) == ' ') c = c.substring(1, c.length);
  			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  		}
  		return null;
  	}
  }]);
}).call(this);
