
angular.module('esgf', ['ngAnimate'])
.controller('ESGFControl', ['$scope', '$http', function($scope, $http) {

  /*
  * Templating Service
  */
  //$scope.newTransaction = tempService();

  window.layout.on( 'new_window', function(template, container){
    console.log(template, container);
    $scope.$apply();
  });

  $scope.init = () => {
    console.log('[+] Initializing ESGF window');
    $scope.step = 0;
    $scope.selected_nodes = undefined;
    $scope.ready = false;
    $scope.datapath = false;
    $scope.facet_options = undefined;
    $scope.searchTerms = {};
    $scope.datasets = {};
    $scope.current_facet = {};
    $scope.facet_cache = {};
    $scope.dataset_cache = {};
    $scope.facet_cache_page_count = {};
    $scope.dataset_cache_page_count = 0;
    $scope.get_node_list();
  }

  $scope.set_datapath = (path) => {
    $scope.datapath = path;
    if(path == 'esgf'){
      $scope.step = 1;
    }
  }


  $scope.search = () => {
    if(Object.keys($scope.searchTerms).length == 0){
      $scope.$parent.showToast('Select at least one facet option');
    } else {
      var params = {
        'searchString': JSON.stringify($scope.searchTerms),
        'nodes': JSON.stringify($scope.selected_nodes)
      }
      $scope.ready = false;
      $http({
        url: 'esgf/node_search',
        method: 'GET',
        params: params
      }).then((res) => {
        console.log('[+] Node search complete');
        console.log(res.data);
        $scope.step = 3;
        $scope.ready = true;
        $scope.datasets = res.data;
        $scope.dataset_cache = $scope.$parent.slice($scope.datasets, 0, 10);
        $scope.dataset_cache_page_count = 1;
      }).catch((res) => {
        console.log('[-] Error during node search');
        console.log(res);
        $scope.$parent.showToast('Error searching selected nodes');
      });
    }
  }

  $scope.show_more_datesets = () => {
    return Object.keys($scope.datasets).length > ($scope.dataset_cache_page_count * 10);
  }

  $scope.next_dataset_page = () => {
    $scope.dataset_cache_page_count = $scope.dataset_cache_page_count + 1;
    $scope.dataset_cache = $scope.$parent.slice($scope.datasets, 0, $scope.dataset_cache_page_count * 10);
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
        $scope.datasets = {};
        $scope.ready = false;
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
      $('#data-select-collapsible').collapsible({
        accordion : false
      });
    }).catch(function(res){
      console.log("[-] Error retrieving node list");
      console.log(res);
      $scope.$parent.showToast('Error retrieving node list');
    });
  }


  $scope.remove_facet = (facet) => {
    delete $scope.searchTerms[facet];
  }

  $scope.show_more_facet_options = (facet) => {
    return Object.keys($scope.facet_options[facet]).length > ($scope.facet_cache_page_count[facet] * 10)
  }

  $scope.next_facet_page = (facet) => {
    $scope.facet_cache_page_count[facet] = $scope.facet_cache_page_count[facet] + 1;
    $scope.facet_cache[facet] = $scope.$parent.slice($scope.facet_options[facet], 0, $scope.facet_cache_page_count[facet] * 10);
  }

  $scope.facet_option_typeahead = (facet) => {
    $scope.switch_arrow(facet);
    if (typeof $scope.facet_cache[facet] === 'undefined') {
      $scope.facet_cache_page_count[facet] = 1;
      $scope.facet_cache[facet] = $scope.$parent.slice($scope.facet_options[facet], 0, 10);
      $scope.setup_bloodhound(Object.keys($scope.facet_options[facet]), facet + '_lookup');

      $('.input-field .typeahead').bind('typeahead:select', function(ev, suggestion) {
        console.log('Selection: ' + suggestion);
        $scope.searchTerms[$(ev.target).parents('.facet_holder').attr('id')] = suggestion;
        $('input[id="' + suggestion + '"]').attr({'checked': true});
        $scope.$apply();
      });
    }
  }

  $scope.setup_bloodhound = (array, id) => {
    var hound = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.whitespace,
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      local: array
    });
    $('#' + id + ' .typeahead').typeahead({
      hint: true,
      highlight: true,
      minLength: 1
    },
    {
      name: id,
      source: hound
    });
  }

  $scope.get_facet_options = () => {
    $http({
      url: 'esgf/load_facets',
      method: 'GET',
      params: {'nodes': JSON.stringify($scope.selected_nodes)}
    }).then((res) => {
      console.log('[+] Got a facet option list');
      console.log(res);
      $scope.ready = true;
      $scope.facet_options = {};
      $scope.facet_options = res.data;
      $scope.datasets = {};
      $scope.searchTerms = {};
      $('.collapsible').collapsible({
        accordion : false
      });
      $scope.setup_bloodhound(Object.keys($scope.facet_options), 'facet_lookup_field');
      $('.typeahead').bind('typeahead:select', function(ev, suggestion) {
        $('#' + suggestion + '_collapsible').trigger('click');
      });
    }).catch((res) => {
      console.log('[-] Error retrieving facet options');
      console.log(res);
      $scope.step = 1;
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
