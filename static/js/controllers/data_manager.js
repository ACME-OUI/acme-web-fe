(function(){
  angular.module('data_manager', ['ngAnimate', 'ngMaterial'])
  .controller('DataManagerControl', function($scope, $http, $timeout, $mdToast) {

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

    $scope.$on('thing', (data) => {
      console.log(data);
    })

    $scope.showToast = function(message) {
      $mdToast.show(
        $mdToast.simple()
          .textContent(message)
          .position('center')
          .hideDelay(1200)
      );
    };

    $scope.open_nc = (file, folder, type) => {
      params = {
        'filename': file,
        'folder': folder,
        'data_type': type
      }
      $http({
        url: '/esgf/read_nc/',
        method: 'GET',
        params: params
      }).then((res)=>{
        $('#text_edit_modal').openModal();
        console.log(res);
        window.ACMEDashboard.ace.setValue(res.data);
        window.ACMEDashboard.ace.setReadOnly(false);
        $('#text_edit_save_btn').addClass('disabled');
      }).catch((res)=>{

      })
    }  

    $scope.set_step = (step) => {
      $scope.step = step;
    }

    $scope.set_favorite_plot = () => {
      var data = {
        'user': window.ACMEDashboard.user,
        'plot': $('#image_download_link_data_manager').attr('data-plot')
      }
      $http({
        url: '/esgf/set_favorite_plot/',
        method: 'POST',
        data: data,
        headers: {
          'X-CSRFToken' : $scope.get_csrf(),
          'Content-Type': 'application/json'
        }
      }).then((res) => {
        $scope.get_favorite_plots();
      }).catch((res) => {

      })
    }

    $scope.get_favorite_plots = () => {
      $http({
        url: '/esgf/get_favorite_plots/',
        method: 'GET'
      }).then((res) => {
        $scope.favorite_plots = res.data;
      }).catch((res) => {

      })
    }

    $scope.get_user = () => {
      $http({
        url: '/run_manager/get_user',
        method: 'GET'
      }).then((res) => {
        window.ACMEDashboard.user = res.data;
        resolve(res.data);
      }).catch((res) => {
        console.log('Error getting user');
        console.log(res);
        reject(res);
      });
    }

    $scope.open_pdf = (diag, diag_folder) => {
      $scope.image_type = 'pdf';
      $scope.diag_folder = diag_folder;
      $scope.show_image = true;
      $scope.image_index = $scope.diag_cache[diag_folder].indexOf(diag);
      var src = $scope.get_src($scope.image_index).then((src) => {
        var image_viewer = $('#pdf_view_data_manager');
        var image_link = $('#image_link_data_manager');
        $('#image_title_data_manager').text(diag);
        image_link.attr({
          'href': src
        });
        $('#image_download_link_data_manager').attr({
          'href': src,
          'download': diag,
          'data-plot': $scope.diag_cache[$scope.diag_folder][$scope.image_index]
        });
        image_viewer.attr({
          'data': src
        });
        $('#image_view_modal_data_manager').openModal();
      }).catch((reason) => {
        console.log('Error: ' + reason);
      })
      
    }

    $scope.open_output = (diag, diag_folder) => {
      $('#image_view_modal_data_manager').openModal();
      $scope.open_image(diag_folder, diag);
    }

    $scope.get_src = (index) => {
      return new Promise((resolve, reject) => {
        if(typeof window.ACMEDashboard.user === 'undefined'){
          $http({
            url: '/run_manager/get_user',
            method: 'GET'
          }).then((res) => {
            window.ACMEDashboard.user = res.data;
            var prefix = '/acme/userdata/image/userdata/' + window.ACMEDashboard.user + '/diagnostic_output/';
            var src = prefix + $scope.diag_folder + '/amwg/' + $scope.diag_cache[$scope.diag_folder][index];
            resolve(src);
          }).catch((res) => {
            console.log('Error getting user');
            console.log(res);
            reject(res);
          });
        } else {
          var prefix = '/acme/userdata/image/userdata/' + window.ACMEDashboard.user + '/diagnostic_output/';
          var src = prefix + $scope.diag_folder + '/amwg/' + $scope.diag_cache[$scope.diag_folder][index];
          resolve(src);
        }
      });
    }

    $scope.open_image = (run, image) => {
      $scope.image_type = 'image';
      $scope.diag_folder = run;
      $scope.show_image = true;
      $scope.image_index = $scope.diag_cache[run].indexOf(image);
      $scope.get_src($scope.image_index).then((src) => {
        var image_viewer = $('#image_view_data_manager');
        var image_link = $('#image_link_data_manager');
        $('#image_title_data_manager').text(image);
        image_link.attr({
          'href': src
        });
        $('#image_download_link_data_manager').attr({
          'href': src,
          'download': image,
          'data-plot': $scope.diag_cache[$scope.diag_folder][$scope.image_index]
        });
        image_viewer.attr({
          'src': src
        });
      }).catch((reason) => {
        console.log("error: " + reason);
      });
    }

    $scope.publish_modal = (data_folder) => {
      $scope.data_folder = data_folder;
      $('#publish_modal').openModal();
      $http({
        url: '/esgf/get_publish_config_list/',
        method: 'GET'
      }).then((res) => {
        console.log(res.data);
        $scope.publish_configs = res.data;
      }).catch((res) => {
        console.log('Error retrieving publication config list');
      });
    }

    $scope.init = () => {
      console.log('[+] Initializing Data Manager window parent scope.id = ' + $scope.$parent.$id);
      $scope.setup_socket();
      $scope.step = -1;
      $scope.selected_nodes = undefined;
      $scope.ready = false; 
      $scope.datapath = false;
      $scope.facet_options = undefined;
      $scope.publish_configs = undefined;
      $scope.facet_list = [0];
      $scope.new_facet_count = 1;
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
      $scope.publish_config_name = 'adsf';
      $scope.diag_limit = 20;
      $scope.obs_limit = 20;
      $timeout(() => {
        $scope.get_user_data();
        $('.collapsible').collapsible({
          accordion : false
        });
      }, 500);
    }

        // The modes
    $scope.modes = ['json'];
    $scope.mode = $scope.modes[0];

    // The ui-ace option
    $scope.aceOption = {
      mode: $scope.mode.toLowerCase(),
      onLoad: function (_ace) {
        window.ACMEDashboard.ace = _ace;
        $scope.modeChanged = function () {
          _ace.getSession().setMode("ace/mode/" + $scope.mode.toLowerCase());
        };

      },
      onChange: function(_ace){
        $scope.aceModel = _ace[1].getValue();
      }
    };

    $scope.new_facet = () => {
      $scope.facet_list.push($scope.new_facet_count++);
    }

    $scope.upload_to_viewer_trigger = (diag_folder) => {
      $scope.diag_folder = diag_folder;
      $('#upload_to_viewer_modal').openModal();
    }

    $scope.upload_to_viewer = () => {
      var data = {
        'run_name': $scope.diag_folder,
        'username': $('#upload_to_viewer_user').val(),
        'password': $('#upload_to_viewer_pass').val(),
        'server': 'http://pcmdi10.llnl.gov:8008/'
      }
      $http({
        url: '/esgf/upload_to_viewer/',
        method: 'POST',
        data: data,
        headers: {
          'X-CSRFToken' : $scope.get_csrf(),
          'Content-Type': 'application/json'
        }
      }).then((res) => {
        console.log(res.data);
        $('#upload_to_viewer_modal').closeModal();
        $scope.showToast('Upload added to run queue');
      }).catch((res) => {
        console.log(res.data);
        $('#upload_to_viewer_modal').closeModal();
        $scope.showToast('Failed to upload to viewer');
      });
    }

    $scope.save_publication_config = () => {
      var params = {
        'config_name': $('#publish_config_name').val(),
        'metadata': {
          'organization': $('#org_name').val(),
          'firstname': $('#publication_author_name_first').val(),
          'lastname': $('#publication_author_name_last').val(),
          'description': $('#publication_description').val(),
          'datanode': $('#publication_datanode').val(),
        },
        'facet': []
      }
      $.each($scope.facet_list, (i, val) => {
        params['facet'].push({
          'name': $('#new_facet_name_' + i).val(),
          'value': $('#new_facet_value_' + i).val()
        });
      });
      $http({
        url: '/esgf/save_publish_config/',
        method: 'POST',
        data: params,
        headers: {
          'X-CSRFToken' : $scope.get_csrf(),
          'Content-Type': 'application/json'
        }
      }).then((res) => {

      }).catch((res) => {

      })
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
      window.ACMEDashboard.notificaiton_list = window.ACMEDashboard.notificaiton_list || [];
      window.ACMEDashboard.socket_handlers = window.ACMEDashboard.socket_handlers || {};
      window.ACMEDashboard.socket_handlers.esgf_download_status = (data) => {
        $scope.$apply(() => {
          console.log('got a status update');
          console.log(data);
          $scope.downloads = $scope.downloads || {};
          $scope.downloads[data.data_name] = $scope.downloads[data.data_name] || {}; 
          $scope.downloads[data.data_name]['percent_complete'] = data.percent_complete.toFixed(2);
          $scope.downloads[data.data_name]['data_name'] = data.data_name;
          $scope.downloads[data.data_name]['message'] = data.message;
        });
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
        if(data.user != window.ACMEDashboard.user){
          return;
        }
        for (key in window.ACMEDashboard.socket_handlers){
          if(!window.ACMEDashboard.socket_handlers.hasOwnProperty(key)){
            continue;
          }
          if(key == data.destination){
            window.ACMEDashboard.socket_handlers[key](data);
          }
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
      $scope.step = -1;
    }

    $scope.get_user = (callback) => {
      $http({
        url: '/run_manager/get_user',
        method: 'GET'
      }).then((res) => {
        $scope.user = res.data
        $scope.get_user_data();
        if(callback){
          callback();
        }
      }).catch((res) => {
        console.log('Error getting user');
        console.log(res);
        if(callback){
          callback();
        }
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
        if($scope.user){
          $scope.set_alldata(res.data[$scope.user]);
        } else {
          $scope.get_user(() => {
            $scope.set_alldata(res.data[$scope.user]);
          });
        }
      }).catch((res) => {
        console.log(res.data);
      });
    }

    $scope.set_alldata = (data) => {
      $scope.all_userdata = data;
      $scope.userdata['model_output'] = Object.keys($scope.all_userdata.model_output);
      $scope.userdata['diagnostic_output'] = Object.keys($scope.all_userdata.diagnostic_output);
      $scope.userdata['observations'] = Object.keys($scope.all_userdata.observations);
      $scope.obs_cache = undefined;
      $scope.diag_cache = undefined;
      $scope.model_cache = undefined;
      $scope.get_favorite_plots();
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
      $scope.diag_cache = $scope.diag_cache || {};      $scope.diag_limit = 20;
      $scope.diag_cache[diag_folder] = Object.keys($scope.all_userdata['diagnostic_output'][diag_folder]['amwg']);
    }
    $scope.increase_diag_limit = () => {
      $scope.diag_limit += 20;
    }
    $scope.increase_obs_limit = () => {
      $scope.obs_limit += 20;
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
  })
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
