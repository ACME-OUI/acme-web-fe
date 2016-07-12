
angular.module('run_manager', [])
.controller('RunManagerControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing RunManager window');
    $scope.ready = false;
    $scope.runs = [];
    $scope.selected_run = undefined;
    $scope.script_list = undefined;
    $scope.get_runs();
  }

  $scope.get_runs = () => {
    $http({
      url: 'run_manager/view_runs'
    }).then((res) => {
      console.log('Got some runs bruh');
      console.log(res.data);
      $scope.run_list = res.data;
      $('#run-list').collapsible({
        accordion : false
      });
      $scope.ready = true;
    }).catch((res) => {
      $scope.ready = true;
      console.log('Failed to get runs');
      console.log(res);
    })
  }

  $scope.modal_trigger = (id) => {
    $('#' + id).openModal();
  }

  $scope.get_run_data = (run) => {
    $scope.switch_arrow(run);
    if($scope.selected_run != run){
      $scope.selected_run = run;
      $http({
        url: 'run_manager/get_scripts',
        params: {
          'run_name' : run
        }
      }).then((res) => {
        console.log('Got some script data');
        console.log(res.data);
        $scope.script_list = res.data;
        if($scope.script_list.length == 0){
          $scope.empty_run = true;
        } else {
          $scope.empty_run = false;
        }
      }).catch((res) => {
        console.log('Error getting script list');
        console.log(res);
      })
    }
  }

  $scope.switch_arrow = (run) => {
    var el = $('#'+run+'_arrow');
    if(el.text() == 'play_arrow'){
      $('#'+run+'_arrow').text('arrow_drop_down');
    } else {
      $('#'+run+'_arrow').text('play_arrow');
    }
  }

}]);
