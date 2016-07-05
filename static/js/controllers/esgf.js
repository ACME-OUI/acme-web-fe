
angular.module('esgf', ['ngAnimate'])
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
    $scope.step = 0;
    $scope.selected_nodes = undefined;
    $scope.ready = false;
    $scope.datapath = false;
    $scope.facet_options = undefined;
    $scope.searchTerms = {};
    $scope.datasets = undefined;
    $scope.spinner = false;
    $scope.current_facet = {};
    $scope.facet_cache = {};
    $scope.get_node_list();
  }

  $scope.set_datapath = (path) => {
    $scope.datapath = path;
    if(path == 'esgf'){
      $scope.step = 1;
    }
  }

  $scope.spinnerToggle = function(on){
    if(on){
      $scope.ready = false;
      $scope.spinner = true;
      var spinner = $('.spinner_wrapper');
      var parent = spinner.parents('.lm_content');
      spinner.css({
        top: (parent.offset().top + parent.height())/2 - spinner.height(),
        left: (parent.offset().left + parent.width())/2 - spinner.width()
      });
    } else {
      $scope.ready = true;
      $scope.spinner = false;
    }
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
      $scope.spinnerToggle(true);
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
        $scope.step = 3;
        $scope.datasets = res.data;
        $scope.spinnerToggle(false);
      }).catch((res) => {
        console.log('[-] Error during node search');
        console.log(res);
        $scope.$parent.showToast('Error searching selected nodes');
        $scope.spinnerToggle(false);
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
        $scope.datasets = undefined;
        $scope.spinnerToggle(true);
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

  $scope.facet_option_typeahead = (facet) => {
    $scope.switch_arrow(facet);
    if (typeof $scope.facet_cache[facet] === 'undefined') {
      $scope.facet_cache[facet] = $scope.facet_options[facet];
      var array = Object.keys($scope.facet_options[facet]);

      console.log(array);
      var options = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: array
      });

      $('#' + facet + '_lookup .typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
      },
      {
        name: facet,
        source: options
      });
      $('.typeahead').bind('typeahead:select', function(ev, suggestion) {
        console.log('Selection: ' + suggestion);
        $scope.searchTerms[facet] = suggestion;
        $('input[id="' + suggestion + '"]').attr({'checked': true});
        $scope.$apply();
      });
    }
  }

  $scope.get_facet_options = () => {
    $http({
      url: 'esgf/load_facets',
      method: 'GET',
      params: {'nodes': JSON.stringify($scope.selected_nodes)}
    }).then((res) => {
      console.log('[+] Got a facet option list');
      console.log(res);
      $scope.spinnerToggle(false);
      $scope.facet_options = {};
      $scope.facet_options = res.data;
      // $scope.facet_options['realm'] = res.data.realm;
      // $scope.facet_options['variable'] = res.data.variable;
      // $scope.facet_options['experiment'] = res.data.experiment;
      //console.log($scope.facet_options);

      $scope.datasets = undefined;
      $scope.searchTerms = {};
      $('.collapsible').collapsible({
        accordion : false
      });
    }).catch((res) => {
      console.log('[-] Error retrieving facet options');
      console.log(res);
      $scope.spinnerToggle(false);
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
