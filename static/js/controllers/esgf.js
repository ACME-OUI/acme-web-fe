
angular.module('esgf', [])
.controller('ESGFControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing ESGF window');
  }

}])
