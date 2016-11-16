
angular.module('cdat', ['ngWebworker'])
.controller('CDATControl', function($scope, $http, $timeout, Webworker, $window) {

    $scope.init = function(){
        console.log('[+] Initializing CDAT window');
        $scope.boxfill = {
            g_name: "Gfb"
        };

        $scope.selected_source = undefined;
        $scope.data_options = undefined;
        $scope.get_user();
        $scope.load_user_data();
        $scope.d_limit = 10;
        $window.rendering = false;
        $scope.rendering = $window.rendering;
        $('.collapsible').collapsible({
            accordion : false
        });
        window.addEventListener('render_complete', (event) => {
            $scope.$apply(() => {
                $scope.rendering = false;
            });
        });
    }

    $scope.deactivate_viz = () => {
        $scope.vizualizer = false;
    }

    $scope.visualize_nc = (file_name, run_name) => {
        var name_split = run_name.split('_');
        var run_name = name_split.slice(0, name_split.length - 1).join('_');
        var run_id = name_split.last();
        var p1 = $http({
            url: '/cdat/get_variables/',
            method: 'POST',
            headers: {
              'X-CSRFToken' : $scope.get_csrf()
            },
            data: {
                'file_name': file_name,
                'run_name': run_name,
                'run_id': run_id
            }
        })
        .then((res) => {
            $scope.variables = res.data;
            $scope.rendering = true;
            $http({
                url: '/cdat/get_provenance/',
                method: 'POST',
                headers: {
                  'X-CSRFToken' : $scope.get_csrf()
                },
                data: {
                    'file_name': file_name,
                    'run_name': run_name,
                    'run_id': run_id,
                    'variable': $scope.variables[0]
                }
            })
            .then((res) => {
                console.log(res.data);
                $scope.vizualizer = 'active';
                $timeout(() => {
                    var vizContainer = $('#vizContainer');
                    var parent = vizContainer.parents('.lm_content');
                    var width = parent.width();
                    var height = parent.height();
                    vizContainer.width(width);
                    vizContainer.height(height);
                    if ($scope.canvas !== undefined) {
                        $scope.canvas.clear();
                    } else {
                        $scope.canvas = vcs.init(document.getElementById('vizContainer'), 'server');
                        vizContainer.on('vcsPlotEnd', function(){
                            $scope.$apply(() => {
                                $scope.rendering = false;
                            });
                        });
                    }
                    $scope.canvas.plot(res.data, $scope.boxfill);
                }, 0, false);
                
            }).catch((res) => {
                console.log(res);
            });
        }).catch((res) => {
            console.log(res);
        });
        
    }

    $scope.select_source = (source) => {
        $scope.selected_source = source;
        if(source == 'diagnostic'){
            $scope.load_diagnostic_data();
        }
        else if(source == 'model'){
            $scope.load_model_data();
        } else {
            console.log('Unrecognized source: ' + source);
            return;
        }
    }

    $scope.load_diagnostic_data = () => {
        // load users available diagnostic data
        if(window.ACMEDashboard.user_data && window.ACMEDashboard.user_data != 'pending'){
            if($scope.select_data = window.ACMEDashboard.user_data[window.ACMEDashboard.user]){
                $scope.select_data = window.ACMEDashboard.user_data[window.ACMEDashboard.user]['diagnostic_output'];
            } else {
                $scope.select_data = window.ACMEDashboard.user_data['diagnostic_output'];
            }
            
            $scope.select_data_keys = Object.keys($scope.select_data);
        } else {
            $timeout(() => {
                $scope.select_data = window.ACMEDashboard.user_data[window.ACMEDashboard.user]['diagnostic_output'];
                $scope.select_data_keys = Object.keys($scope.select_data);
            }, 500);
        }
        
    };

    $scope.load_model_data = () => {
        // load users available model data
        if(window.ACMEDashboard.user_data && window.ACMEDashboard.user_data != 'pending'){
            if($scope.select_data = window.ACMEDashboard.user_data[window.ACMEDashboard.user]){
                $scope.select_data = window.ACMEDashboard.user_data[window.ACMEDashboard.user]['model_output'];
            } else {
                $scope.select_data = window.ACMEDashboard.user_data['model_output'];
            }
            
            $scope.select_data_keys = Object.keys($scope.select_data);
        } else {
            $timeout(() => {
                $scope.select_data = window.ACMEDashboard.user_data[window.ACMEDashboard.user]['model_output'];
                $scope.select_data_keys = Object.keys($scope.select_data);
            }, 500);
        }
    };

    $scope.increase_d_limit = (all) => {
        if(all){
            $scope.d_limit = $scope.selected_data_options.length;
        } else {
            $scope.d_limit += 10;
        }
    }

    $scope.select_data_option = (data) => {
        if($scope.selected_data_option == data){
            return;
        } else {
            $scope.selected_data_option = data;
            $scope.selected_data_options = [];
            if($scope.selected_source == 'diagnostic'){
                for(k in $scope.select_data[data]['amwg']){
                    if(k.endsWith('.nc')){
                        $scope.selected_data_options.push(k);
                    }
                }
            } else {
                for(k in $scope.select_data[data]){
                    if(k.endsWith('.nc')){
                        $scope.selected_data_options.push(k);
                    }
                }
            }

            $('.collapsible').collapsible({
                accordion : false
            });
        }

    }

    $scope.load_user_data = () => {
        if(window.ACMEDashboard.user_data){
            return;
        } else {
            window.ACMEDashboard.user_data = 'pending';
        }
        var worker = Webworker.create(window.ACMEDashboard.ajax, {async: true });
        var data = {
            'url': 'http://' + window.location.hostname + ':8000/esgf/get_user_data',
            'method': 'GET'
        };
        worker.run(data).then((result) => {
            $scope.user_data = JSON.parse(result);
            window.ACMEDashboard.user_data = $scope.user_data;
        }).catch((res) => {
            console.log(res);
        });
    }

    $scope.get_user = () => {
        if(window.ACMEDashboard.user){
            return;
        } else {
            window.ACMEDashboard.user = 'pending';
        }
        var worker = Webworker.create(window.ACMEDashboard.ajax, {async: true });
        var data = {
            'url': 'http://' + window.location.hostname + ':8000/run_manager/get_user/',
            'method': 'GET'
        };
        worker.run(data).then((result) => {
            window.ACMEDashboard.user = result;
        }).catch((res) => {
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
})
.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
});
