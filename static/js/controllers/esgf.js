
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

  $scope.arrFromMyObj = (obj) => {
      Object.keys(obj).map(function(key) {
        return obj[key];
      });
  };

  $scope.search = () => {
    if(Object.keys($scope.searchTerms).length == 0){
      $scope.$parent.showToast('Select at least one facet option');
    } else {
      $scope.ready = false;
      $scope.spinner = true;
      var spinner = $('.spinner_wrapper');
      var parent = spinner.parents('.lm_content');
      spinner.css({
        top: (parent.offset().top + parent.height())/2 - spinner.height(),
        left: (parent.offset().left + parent.width())/2 - spinner.width()
      });
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
        $scope.spinner = false;
      }).catch((res) => {
        console.log('[-] Error during node search');
        console.log(res);
        $scope.ready = true;
        $scope.$parent.showToast('Error searching selected nodes');
        $scope.spinner = false;
      });
    }
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
        $scope.step = 2;
        $scope.ready = false;
        $scope.datasets = undefined;
        $scope.get_facet_options();
      } else {
        $scope.$parent.showToast('Select at least one data node')
      }
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

  $scope.remove_facet = (facet) => {
    delete $scope.searchTerms[facet];
  }

  $scope.get_facet_options = () => {
    $scope.spinner = true;
    var spinner = $('.spinner_wrapper');
    spinner.css({
      top: (spinner.parents('.lm_content').offset().top + spinner.parent().height())/2 - spinner.height(),
      left: (spinner.parents('.lm_content').offset().left + spinner.parent().width())/2 - spinner.width()
    });
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
      $scope.datasets = undefined;
      $scope.searchTerms = {};
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
