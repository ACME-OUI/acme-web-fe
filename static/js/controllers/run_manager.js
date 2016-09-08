(function(){
  angular.module('run_manager', ['ui.ace', 'ngMaterial'])
  .controller('RunManagerControl', ['$scope', '$http', '$timeout', '$mdToast', function($scope, $http, $timeout, $mdToast) {

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

    $scope.get_user = () => {
      $http({
        url: '/run_manager/get_user',
        method: 'GET'
      }).then((res) => {
        $scope.$parent.user = res.data
      }).catch((res) => {
        console.log('Error getting user');
        console.log(res);
      });
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

    $scope.init = function(){
      console.log('[+] Initializing RunManager window');
      $scope.setup_socket();
      $scope.$on('notification', (data) => {
        console.log('got a notification')
      })
      $scope.run_options = ['New run configuration', 'start run', 'stop run', 'update status', 'new template'];
      $scope.run_types = ['diagnostic', 'model'];
      $scope.aceModel = '';
      $scope.ready = false;
      $scope.run_list = [];
      $scope.all_runs = undefined;
      $scope.selected_run = undefined;
      $scope.script_list = undefined;
      $scope.output_list = [];
      $scope.output_cache = {};
      $scope.output_cache_count = {};
      $scope.template_list = undefined;
      $scope.show_image = false;
      $scope.image_index = 0;
      $scope.selected_run_params = {};
      $scope.get_templates();
      $scope.get_runs();
      $scope.get_user();
      $scope.get_run_status();
      document.onkeydown = checkKey;

      function checkKey(e) {
        if($scope.show_image){
          e = e || window.event;

          if (e.keyCode == '37') {
            if($scope.image_index > 0){
              $scope.image_index -= 1;
              if($scope.show_image_by_index($scope.image_index)){
                $scope.image_index += 1;
              }

            }
          }
          else if (e.keyCode == '39') {
            if($scope.image_index < $scope.output_list[$scope.selected_run].length){
              $scope.image_index += 1;
              if($scope.show_image_by_index($scope.image_index)){
                $scope.image_index -= 1;
              }
            }
          }
        }
      }
    }

    $scope.setup_socket = () => {
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      if(!window.ACMEDashboard.socket){
        window.ACMEDashboard.socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
      }
      window.ACMEDashboard.socket_handlers = window.ACMEDashboard.socket_handlers || {};
      window.ACMEDashboard.socket_handlers.set_run_status = (data) => {
        console.log('got a status update');
        $scope.$emit('notification', {'message': data});
        var job = $scope.all_runs.filter((obj) => {
          return obj.job_id == data.job_id
        });
        // if(job.length == 0){
        //   var optional_message = JSON.parse(data.optional_message);
        //   var run_name = optional_message.run_name;
        //   var job = {
        //     'run_name': 'upload_to_viewer',
        //     'job_id': data.job_id
        //   }
        //   if(run_name){
        //     job.run_name = run_name;
        //   }
        //   $scope.all_runs.push(job);
        // }
        $scope.set_status_text(data.status, data.job_id + "_queue");
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
        if(data.user != $scope.$parent.user){
          return;
        }
        var data = JSON.parse(message.data);
        if(data.user != $scope.$parent.user){
          return;
        }
        for(key in window.ACMEDashboard.socket_handlers){
          if(!window.ACMEDashboard.socket_handlers.hasOwnProperty(key)){
            continue;
          }
          if(key == data.destination){
            window.ACMEDashboard.socket_handlers[key](data);
            break;
          }
        }
        $scope.$apply();
      }
    }

    $scope.show_image_by_index = (index) => {
      if(!$scope.output_list[$scope.selected_run][index].endsWith('.png')){
        return true;
      }
      var src = $scope.get_src(index);
      var image_viewer = $('#image_view');
      var image_link = $('#image_link');
      $('#image_title').text($scope.output_list[$scope.selected_run][index]);
      image_link.attr({
        'href': src
      });
      $('#image_download_link').attr({
        'href': src
      });
      image_viewer.attr({
        'src': src
      });
    }

    $scope.get_src = (index) => {
      var prefix = '/acme/userdata/image/userdata/' + $scope.$parent.user + '/diagnostic_output/';
      var src = prefix + $scope.selected_run + '/diagnostic_output/amwg/' + $scope.output_list[$scope.selected_run][index];
      return src;
    }

    $scope.open_image = (run, image) => {
      $scope.show_image = true;
      $scope.image_index = $scope.output_list[$scope.selected_run].indexOf(image);
      var image_el = $('#' + run + '_' + image.slice(0,20));
      //var src = image_el.attr('data-img-location');
      var src = $scope.get_src($scope.image_index);
      var image_viewer = $('#image_view');
      var image_link = $('#image_link');
      $('#image_title').text(image);
      image_link.attr({
        'href': src
      });
      $('#image_download_link').attr({
        'href': src,
        'download': image
      });
      image_viewer.attr({
        'src': src
      });

      $('#image_view_modal').openModal();
    }

    // The modes
    $scope.modes = ['json'];
    $scope.mode = $scope.modes[0];

    $scope.load_output_cache = () => {
      $scope.output_cache_count[$scope.selected_run] += 1;
      $scope.output_cache[$scope.selected_run] = $scope.output_list[$scope.selected_run].slice(0, $scope.output_cache_count[$scope.selected_run] * 10);
    }


    // The ui-ace option
    $scope.aceOption = {
      mode: $scope.mode.toLowerCase(),
      onLoad: function (_ace) {
        $scope.ace = _ace;
        $scope.modeChanged = function () {
          _ace.getSession().setMode("ace/mode/" + $scope.mode.toLowerCase());
        };

      },
      onChange: function(_ace){
        $scope.aceModel = _ace[1].getValue();
      }
    };

    $scope.set_run_status = (data) => {
      for(obj in data){
        //$scope.set_status_text(data[obj].status, data[obj].run_name);
        $scope.set_status_text(data[obj].status, data[obj].job_id + "_queue");
      }
    }

    $scope.trigger_option = (option) => {
      if(option == 'New run configuration'){
        $scope.get_templates();
        $scope.modal_trigger('new_run_modal');
      } else if (option == 'start run') {
        $scope.modal_trigger('start_run_modal');
      } else if (option == 'stop run') {
        $scope.modal_trigger('stop_run_modal');
      } else if (option == 'update status') {
        $scope.get_run_status($scope.set_run_status);
      } else if (option == 'new template') {
        $scope.template_select_options();
      }
    }

    $scope.open_text_edit = (run, script) => {
      $('#text_edit_modal').openModal();
      $scope.selected_script = script;
      var data = {
        'run_name': run,
        'script_name': script
      }
      $http({
        url: '/run_manager/read_script/',
        method: 'GET',
        params: data
      }).then((res) => {
        console.log(res);
        var script = JSON.stringify(JSON.parse(res.data.script), null, 2);
        //$scope.aceModel = script;
        $scope.ace.setValue(script);
        $scope.ace.setReadOnly(false);
        $('#text_edit_save_btn').removeClass('disabled');
      }).catch((res) => {
        console.log(res);
      })
    }

    $scope.update_script = () => {
      var data = {
        'script_name': $scope.selected_script,
        'run_name': $scope.selected_run,
        'contents': $scope.aceModel
      }
      $http({
        url: '/run_manager/update_script/',
        method: 'POST',
        data: data,
        headers: {
          'X-CSRFToken' : $scope.get_csrf()
        }
      }).then((res) => {
        console.log(res);
        $scope.showToast("File saved");
        $('#text_edit_modal').closeModal();
      }).catch((res) => {
        console.log(res);
      })
    }

    $scope.stop_run = (run) => {
      $http({
        url: '/run_manager/stop_job/',
        method: 'POST',
        data: {
          "job_id": run.job_id,
          "request": 'stop'
        },
        headers: {
          'X-CSRFToken' : $scope.get_csrf()
        }
      }).then((res) => {
        $scope.get_run_status();
      }).catch((res) => {
        $scope.showToast('Error stopping run ' + run.run_name);
      })
    }


    $scope.get_run_status = (callback) => {
      $http({
        url: '/run_manager/run_status/',
        method: 'GET'
      }).then((res) => {
        var runs = res.data;
        if(Object.keys(runs).length !== 0){
          runs.sort(function(a, b){
            return a.job_id - b.job_id
          });
        }
        if($scope.all_runs){
          for(r in runs){
            if($scope.all_runs[r] && $scope.all_runs[r].job_id == runs[r].job_id){
              $scope.all_runs[r].status = runs[r].status;
            } else {
              $scope.all_runs.push(runs[r]);
            }
          }
        } else {
          $scope.all_runs = runs;
        }
        $timeout($scope.set_run_status, delay=200, true, runs);
        if(callback){
          callback();
        }
      }).catch((res) => {
        $scope.showToast("error getting run status");
        if(callback){
          callback();
        }
      });
    }

    $scope.create_run = (template) => {
      var run_name = $('#new_run_name').val();
      if(!run_name || run_name.length == 0){
        $scope.showToast('New run requires a name');
        return;
      }
      var run_type = $('#run_type_radio_select input:checked').attr('data-run-type');
      if(!run_type || run_type.length == 0){
        $scope.showToast('New run requires a type');
        return;
      }

      if(template){
        params = {
          'run_name': run_name,
          'run_type': run_type,
          'template': template,
        }
      } else {
        params = {
          'run_name': run_name,
          'run_type': run_type,
        }
      }
      $http({
        url: '/run_manager/create_run/',
        data: params,
        method: 'POST',
        headers: {
          'X-CSRFToken' : $scope.get_csrf()
        }
      }).then((res) => {
        console.log('created a new run');
        console.log(res.data);
        if('error' in res.data){
          $scope.showToast(res.data['error']);
          return;
        }
        $scope.run_list.push(run_name);
        $('#new_run_modal').closeModal();
        $('#new_run_name').val('');
        //$scope.$apply();
      }).catch((res) => {
        console.log('Error creating new run');
        console.log(res.data);
        $scope.showToast('Error creating new run');
      });
    }

    $scope.get_runs = () => {
      return new Promise(function(resolve, reject){
        $http({
          url: '/run_manager/view_runs'
        }).then((res) => {
          console.log('Got some runs bruh');
          console.log(res.data);
          $scope.run_list = res.data;
          $('#run-list').collapsible({
            accordion : false
          });
          $scope.ready = true;
          resolve(res.data);
        }).catch((res) => {
          $scope.ready = true;
          console.log('Failed to get runs');
          console.log(res);
          reject(res.data);
        });
      });
    }

    $scope.template_select_options = () => {
      $scope.modal_trigger('copy_template_modal');
      $scope.get_templates();
    }

    $scope.set_status_text = (status, run_name) => {
      var el = $('#' + run_name + '_status');
      switch(status){
        case "new":
          el.css({'color': '#009688'});
          el.text('waiting in queue');
          break;
        case "in_progress":
          el.css({'color': '#4caf50'});
          el.text('running');
          break;
        case "complete":
          el.css({'color': '#2196f3'});
          el.text('complete');
          break;
        case "failed":
          el.css({'color': '#d32f2f'});
          el.text('error');
          break;
        case "stopped":
          el.css({'color': '#ffd600'});
          el.text('stopped');
          break;
        default:
          el.css({'color': '#9e9e9e'});
          el.text('idle');
      }
    }

    $scope.start_run = (run) => {
      console.log('attempting to start run ' + run);
      $http({
        url: '/run_manager/start_run/',
        method: 'POST',
        data: {'run_name': run},
        headers: {
          'X-CSRFToken' : $scope.get_csrf()
        }
      }).then((res) => {
        $scope.get_run_status();
        $scope.set_status_text('new', run);
        $scope.showToast("Run added to the queue");
        $('#start_run_modal').closeModal();
        //$scope.get_run_status($scope.set_run_status);
      }).catch((res) => {
        $scope.showToast('Failed to start run');
        $('#start_run_modal').closeModal();
      });
    }

    $scope.get_templates = () => {
      $http({
        url: '/run_manager/get_templates'
      }).then((res) => {
        console.log('Got a list of templates');
        console.log(res.data);
        $scope.template_list = res.data;
        //$('#copy_template_modal').height($('#template_collection').height())
      }).catch((res) => {
        console.log('error getting template list');
        console.log(res);
      });
    }

    $scope.create_new_template_edit = () => {

    }

    $scope.modal_trigger = (id) => {
      $('#' + id).openModal();
      $('.modal').css({'bottom': 'inherit'});
    }

    $scope.select_template = (template) => {
      var new_template_name = $('#new_template_name').val();
      if(!new_template_name || new_template_name.length == 0){
        $scope.showToast('Copy template requires a name');
        return;
      }
      $http({
        url: '/run_manager/copy_template/',
        method: 'POST',
        headers: {
          'X-CSRFToken' : $scope.get_csrf()
        },
        data: {
          template: template,
          new_template: new_template_name
        }
      }).then((res) => {
        console.log('successfully copied template');
        $('copy_template_modal').closeModal();
        $('#new_template_name').val('');
        $scope.showToast('Successfully copied template');
      }).catch((res) => {
        console.log('Error copying template');
        $scope.showToast('Error copying template');
      });
    }

    $scope.get_run_data = (run, job_id) => {
      $scope.switch_arrow(run);
      var run_name = '';
      if(job_id){
        run_name = run + '_' + job_id
      } else {
        run_name = run
      }
      if($scope.selected_run == run_name){
        return;
      } else {
        $scope.selected_run = run_name;
        $http({
          url: '/run_manager/get_scripts',
          params: {
            'run_name' : run,
            'job_id': job_id
          }
        }).then((res) => {
          $timeout(() => {
            console.log('Got some script data');
            console.log(res.data);
            $scope.script_list = res.data.script_list;
            $scope.output_list[$scope.selected_run] = [];
            $scope.output_list[$scope.selected_run] = res.data.output_list;
            if($scope.script_list.length == 0){
              $scope.empty_run = true;
            } else {
              $scope.empty_run = false;
            }

            if($scope.output_list[$scope.selected_run].length != 0){
              $scope.output_cache_count[$scope.selected_run] = 0;
              $scope.load_output_cache();
            }
            $('.collapsible').collapsible({
              accordion : false
            });
          }, delay=200);
        }).catch((res) => {
          console.log('Error getting script list');
          console.log(res);
        })
      }
    }

    $scope.open_output = (run, item, job_id) => {
      if(item.endsWith('.png')){
        $scope.open_image(run, item);
      }
      else if (item.endsWith('.txt')) {
          $('#text_edit_modal').openModal();
          $scope.selected_script = item;
          var data = {
            'run_name': run,
            'script_name': item,
            'job_id': job_id
          }
          $http({
            url: '/run_manager/read_output_script/',
            method: 'GET',
            params: data
          }).then((res) => {
            console.log(res);
            var script = res.data.script;
            $scope.aceModel = script;
            $scope.ace.setValue(script);
            $scope.ace.setReadOnly(true);
            $('#text_edit_save_btn').addClass('disabled');
          }).catch((res) => {
            console.log(res);
          });
      }
    }

    $scope.switch_arrow = (id) => {
      var el = $('#'+ id +'_arrow');
      if(el.text() == 'play_arrow'){
        $('#'+ id +'_arrow').text('arrow_drop_down');
      } else {
        $('#'+ id +'_arrow').text('play_arrow');
      }
    }

  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
