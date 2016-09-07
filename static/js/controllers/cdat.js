
angular.module('cdat', [])
.controller('CDATControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing CDAT window');
  }

  $scope.new_plot = function new_plot(id, plotvars) {
		console.log("making cdat window");

		
	}
}])
