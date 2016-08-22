(function(){
  angular.module('data_manager', ['ngAnimate', 'ngMaterial'])
  .controller('DataManagerControl', ['$scope', '$http', '$timeout', '$mdToast', function($scope, $http, $timeout, $mdToast) {

    /**
     * Slices the object. Note that returns a new spliced object,
     * e.g. do not modifies original object. Also note that that sliced elements
     * are sorted alphabetically by object property name.
     * see: http://stackoverflow.com/a/20682709
     */
    $scope.slice = (obj, start, end) => {
        var sliced = {};
        var i = 0;
        for (var k in obj) {
            if (i >= start && i < end)
                sliced[k] = obj[k];
            i++;
        }
        return sliced;
    }

    $scope.showToast = function(message) {
      $mdToast.show(
        $mdToast.simple()
          .textContent(message)
          .position('center')
          .hideDelay(1200)
      );
    };

    $scope.set_step = (step) => {
      $scope.step = step;
      console.log(step);
    }

    $scope.init = () => {
      //alert('running init')
      console.log('[+] Initializing Data Manager window');
      $scope.step = -1;
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
      $timeout(() => {
        $('.collapsible').collapsible({
          accordion : false
        });
      }, 200);

    }

    $scope.set_datapath = (path) => {
      $scope.datapath = path;
      if(path == 'esgf'){
        $scope.step = 1;
      }
    }

    $scope.search = () => {
      if(Object.keys($scope.searchTerms).length == 0){
        $scope.showToast('Select at least one facet option');
      } else {
        var params = {
          'searchString': JSON.stringify($scope.searchTerms),
          'nodes': JSON.stringify($scope.selected_nodes)
        }
        $scope.ready = false;
        $http({
          url: '/esgf/node_search',
          method: 'GET',
          params: params
        }).then((res) => {
          console.log('[+] Node search complete');
          console.log(res.data);
          $scope.step = 3;
          $scope.ready = true;
          $scope.datasets = res.data;
          $scope.dataset_cache = $scope.slice($scope.datasets, 0, 10);
          $scope.dataset_cache_page_count = 1;
        }).catch((res) => {
          console.log('[-] Error during node search');
          console.log(res);
          $scope.showToast('Error searching selected nodes');
        });
      }
    }

    $scope.show_more_datesets = () => {
      return Object.keys($scope.datasets).length > ($scope.dataset_cache_page_count * 10);
    }

    $scope.next_dataset_page = () => {
      $scope.dataset_cache_page_count = $scope.dataset_cache_page_count + 1;
      $scope.dataset_cache = $scope.slice($scope.datasets, 0, $scope.dataset_cache_page_count * 10);
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
          $scope.showToast('Select at least one data node')
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
        url: '/esgf/node_list',
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
        $scope.showToast('Error retrieving node list');
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
      $scope.facet_cache[facet] = $scope.slice($scope.facet_options[facet], 0, $scope.facet_cache_page_count[facet] * 10);
    }

    $scope.facet_option_typeahead = (facet) => {
      $scope.switch_arrow(facet);
      if (typeof $scope.facet_cache[facet] === 'undefined') {
        $scope.facet_cache_page_count[facet] = 1;
        $scope.facet_cache[facet] = $scope.slice($scope.facet_options[facet], 0, 10);
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
        url: '/esgf/load_facets',
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
        $scope.showToast('Error retrieving facet options');
      });
    }
  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
