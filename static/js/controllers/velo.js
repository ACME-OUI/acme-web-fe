
angular.module('velo', [])
.controller('VeloControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing Velo window');
  }

}])
