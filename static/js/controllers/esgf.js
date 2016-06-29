
angular.module('esgf', [])
.controller('ESGFControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing ESGF window');
  }

  function Parent($scope) {
    $scope.treedata=createSubTree(3, 4, "");
    $scope.lastClicked = null;
    $scope.buttonClick = function($event, node) {
        $scope.lastClicked = node;
        $event.stopPropagation();
    }
    $scope.showSelected = function(sel) {
        $scope.selectedNode = sel;
    };
  }

}])
