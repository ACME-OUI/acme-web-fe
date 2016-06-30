
angular.module('esgf', [])
.controller('ESGFControl', ['$scope', '$http', function($scope, $http) {

  /*
  * Templating Service
  */
  //$scope.newTransaction = tempService();

  // window.layout.on( 'new_window', function(template, container){
  //   console.log(template, container);
  //   //$compile(container.contents())(scope);
  // });

  $scope.init = () => {
    console.log('[+] Initializing ESGF window');
    $scope.step = 1;
    $scope.selected_nodes = undefined;
    $scope.ready = false;
    $scope.facet_options = undefined;
    $scope.searchTerms = {};
    $scope.datasets = undefined;
    $scope.spinner = false;
    $scope.get_node_list();
  }

  $scope.search = () => {
    $scope.ready = false;
    var params = {
      'searchString': JSON.stringify($scope.searchTerms),
      'nodes': JSON.stringify($scope.selected_nodes)
    }
    $http({
      url: 'esgf/node_search',
      method: 'GET',
      params: params
    }).then((res) => {
      console.log('[+] Node search complete');
      console.log(res.data);
      $scope.ready = true;
      $scope.step = 3;
      $scope.datasets = res.data;
    }).catch((res) => {
      console.log('[-] Error during node search');
      console.log(res);
      $scope.ready = true;
      $scope.$parent.showToast('Error searching selected nodes');
    })
  }

  $scope.select_nodes = (id) => {
    console.log(id);
    $scope.selected_nodes = [];
    $.each($('.esgf_scope_'+id+' input:checked'), (i, val) => {
        $scope.selected_nodes.push($(val).val());
    })
    .promise()
    .done(() =>{
      if($scope.selected_nodes.length > 0){
        $scope.nodes_been_selected = true;
      } else {
        $scope.$parent.showToast('Select at least one data node')
      }
      $scope.ready = false;
      $scope.get_facet_options();
    });
  };

  $scope.deselect_node = (node) => {
    console.log(node);
  }

  $scope.switch_arrow = (facet) => {
    var el = $('#'+facet+'_arrow');
    if(el.text() == 'play_arrow'){
      $('#'+facet+'_arrow').text('arrow_drop_down');
    } else {
      $('#'+facet+'_arrow').text('play_arrow');
    }

  }

  $scope.get_node_list = () => {
    $http({
      url: 'esgf/node_list',
      method: 'GET'
    }).then(function(res){
      $scope.node_list = res.data
      $scope.ready = true;
    }).catch(function(res){
      console.log("[-] Error retrieving node list");
      console.log(res);
      $scope.$parent.showToast('Error retrieving node list');
    });
  }

  $scope.get_facet_options = () => {
    $scope.spinner = true;
    $http({
      url: 'esgf/load_facets',
      method: 'GET',
      params: {'nodes': JSON.stringify($scope.selected_nodes)}
    }).then((res) => {
      console.log('[+] Got a facet option list');
      console.log(res);
      $scope.ready = true;
      $scope.spinner = false;
      $scope.facet_options = res.data;
      $('.collapsible').collapsible({
        accordion : false
      });
      $scope.step = 2;
    }).catch((res) => {
      console.log('[-] Error retrieving facet options');
      console.log(res);
      $scope.ready = true;
      $scope.$parent.showToast('Error retrieving facet options');
    });
  }

}]);
// .directive( 'compileData', function ( $compile ) {
//   return {
//     scope: true,
//     link: function ( scope, element, attrs ) {
//
//       var elmnt;
//
//       attrs.$observe( 'template', function ( myTemplate ) {
//         if ( angular.isDefined( myTemplate ) ) {
//           // compile the provided template against the current scope
//           elmnt = $compile( myTemplate )( scope );
//
//             element.html(""); // dummy "clear"
//
//           element.append( elmnt );
//         }
//       });
//     }
//   };
// })
// .factory( 'tempService', function () {
//   return function () {
//     return '<div class="esgf_window" ng-controller="ESGFControl" ng-init="init()">'+
//               '<form class="dashboard-show-hide" ng-show="nodes_been_selected == false">'+
//                 '<p ng-repeat="node in node_list">'+
//                   '<input type="checkbox" id="[[node + $id]]" />'+
//                   '<label for="[[node + $id]]">[[node]]</label>'+
//                 '</p>'+
//                 '<a class="waves-effect waves-light btn" ng-click="select_nodes($id)"> select </a>'+
//               '</form>'+
//               '<div class="dashboard-show-hide" ng-show="nodes_been_selected == true">'+
//                 '<a class="waves-effect waves-light btn" ng-click="nodes_been_selected = false">'+
//                   '<i class="material-icons left">ic_arrow_back</i>'+
//                 '</a>'+
//                 '<br>'+
//                 '<treecontrol class="tree-classic" tree-model="treedata" on-selection="showSelected(node)">'+
//                   '<button ng-click="buttonClick($event, node)">Click Me!</button> label: [[node.label]] ([[node.id]] ) [[$index]]'+
//                 '</treecontrol>'+
//               '</div>'+
//             '</div>';
//   };
// });
