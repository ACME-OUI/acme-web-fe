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
    }

    $scope.publish = (diag_folder) => {
      $scope.diag_folder = diag_folder;
      $('#publish_modal').openModal();
    }

    $scope.init = () => {
      console.log('[+] Initializing Data Manager window');
      $scope.setup_socket();
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
      $scope.userdata = {};
      $scope.get_user();
      $scope.get_node_list();
      $timeout(() => {
        $scope.get_user_data();
        $('.collapsible').collapsible({
          accordion : false
        });
      }, 200);
    }

    $scope.get_csrf = () => {
      var cookieValue = null;
      var name = 'csrftoken';
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }

    $scope.download_modal = () => {
      $('#download_dataset_modal').openModal();
    }
    $scope.upload_modal = () => {
      $('#file_upload_modal').openModal();
    }
    $scope.upload_file = () => {
      var name = $('#upload_name').val();
      var type = $('#upload_type_radio_select input:checked').attr('data-upload-type');
      var file = new FormData();
      $.each(document.getElementById('file-upload-picker').files, (i, obj) => {
        file.append(name, obj);
      })
      file.append('type', type);
      $http({
        url: '/esgf/file_upload/',
        method: 'POST',
        data: file,
        processData: false,
        contentType: false,
        dataType: 'json',
        transformRequest: angular.identity,
        headers: {
          'X-CSRFToken' : $scope.get_csrf(),
          'Content-Type': undefined
        }
      }).then((res) =>{
        console.log('successfully uploaded file');
        $scope.showToast('successfully uploaded file');
        $('#file_upload_modal').closeModal();
        $scope.get_user_data();
      }).catch((res) => {
        $scope.showToast('File upload error');
        $('#file_upload_modal').closeModal();
        console.log('file upload failure');
      });
    }
    $scope.setup_socket = () => {
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      if(!window.ACMEDashboard.socket){
        window.ACMEDashboard.socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
      }
      window.ACMEDashboard.socket.onopen = function() {
        message = JSON.stringify({
          'target_app': 'run_manager',
          'destination': 'init',
          'content': 'hello world!'
        })
        window.ACMEDashboard.socket.send(message);
      }
      window.ACMEDashboard.socket.onmessage = (message) => {
        var data = JSON.parse(message.data);
        if(data.user != $scope.user){
          return;
        }
        switch (data.destination) {
          case 'esgf_download_status':
            console.log('got a status update');
            console.log(data);
            $scope.downloads = $scope.downloads || {};
            $scope.downloads[data.data_name] = $scope.downloads[data.data_name] || {}; 
            $scope.downloads[data.data_name]['percent_complete'] = data.percent_complete.toFixed(2);
            $scope.downloads[data.data_name]['data_name'] = data.data_name;
            $scope.downloads[data.data_name]['message'] = data.message;
            $scope.$apply();
            break;
          default:

        }
      }
    }

    $scope.download_dataset = () => {
      var params = {
        'data_type': $('#download_type_radio_select input:checked').attr('data-download-type'),
        'data_name': $('#download_name').val(),
        'openid_username': $('#openid_username').val(),
        'openid_password': $('#openid_password').val(),
        'search_string': $scope.searchTerms,
        'nodes': $scope.selected_nodes,
      };
      request = JSON.stringify({
        'target_app': 'esgf',
        'destination': 'dataset_download',
        'params': params,
        'user': $scope.user
      })
      window.ACMEDashboard.socket.send(request);
      $scope.downloads = $scope.downloads || {};
      $scope.downloads[params.data_name] = {
        'percent_complete': 0
      };      
      $('#download_modal').closeModal();
    }

    $scope.get_user = () => {
      $http({
        url: '/run_manager/get_user',
        method: 'GET'
      }).then((res) => {
        $scope.user = res.data
        $scope.get_user_data();
      }).catch((res) => {
        console.log('Error getting user');
        console.log(res);
      });
    }

    $scope.set_datapath = (path) => {
      $scope.datapath = path;
      if(path == 'esgf'){
        $scope.step = 1;
      }
    }

    $scope.get_user_data = () => {
      $http({
        url: '/esgf/get_user_data'
      }).then((res) => {
        console.log(res.data);
        $scope.all_userdata = res.data[$scope.user]
        $scope.userdata['model_output'] = Object.keys($scope.all_userdata.model_output);
        $scope.userdata['diagnostic_output'] = Object.keys($scope.all_userdata.diagnostic_output);
        $scope.userdata['observations'] = Object.keys($scope.all_userdata.observations);
        $scope.obs_cache = undefined;
        $scope.diag_cache = undefined;
        $scope.model_cache = undefined;
      }).catch((res) => {
        console.log(res.data);
      })
    }

    $scope.load_obs_cache = (obs_folder) => {
      $scope.obs_cache = $scope.obs_cache || {};
      $scope.obs_cache[obs_folder] = Object.keys($scope.all_userdata['observations'][obs_folder]);
    }
    $scope.load_model_cache = (model_folder) => {
      $scope.model_cache = $scope.model_cache || {};
      $scope.model_cache[model_folder] = Object.keys($scope.all_userdata['model_output'][model_folder]);
    }
    $scope.load_diag_cache = (diag_folder) => {
      $scope.diag_cache = $scope.diag_cache || {};
      $scope.diag_cache[diag_folder] = Object.keys($scope.all_userdata['diagnostic_output'][diag_folder]['diagnostic_output']['amwg']);
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

    $scope.get_keys = (obj) => {
      if(obj){
        return Object.keys(obj);  
      }
      return false;
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
