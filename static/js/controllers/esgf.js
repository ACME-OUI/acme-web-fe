
angular.module('esgf', [])
.controller('ESGFControl', ['$scope', '$http', '$element', function($scope, $http, $element) {

  $scope.init = () => {
    console.log('[+] Initializing ESGF window');
    $scope.nodes_been_selected = false;
    $scope.selected_nodes = undefined;
    $http({
      url: 'esgf/node_list',
      method: 'GET'
    }).then(function(res){
      $scope.node_list = res.data
    }).catch(function(res){
      console.log("[-] Error retrieving node list");
      console.log(res);
    });
  }

  $scope.select_nodes = (id) => {
    $scope.selected_nodes = [];
    $.each($('input:checked'), (i, val) => {
        $scope.selected_nodes.push($(val).val());
    })
    .promise()
    .done(() =>{
      if($scope.selected_nodes.length > 0){
        $scope.nodes_been_selected = true;
      } else {
        $scope.$parent.showToast('Select at least one data node')
      }
    });

  }

  function Parent($scope) {
    $scope.treedata=createSubTree(3, 4, "");
    $scope.lastClicked = null;
    $scope.buttonClick = ($event, node) => {
        $scope.lastClicked = node;
        $event.stopPropagation();
    }
    $scope.showSelected = (sel) => {
        $scope.selectedNode = sel;
    };
  }

}])
