
angular.module('run_manager', [])
.controller('RunManagerControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing RunManager window');
    $scope.run_options = ['New run configuration', 'start run', 'stop run', 'run status'];
    $scope.ready = false;
    $scope.run_list = [];
    $scope.selected_run = undefined;
    $scope.script_list = undefined;
    $scope.template_list = undefined;
    $scope.get_runs();
  }

  $scope.trigger_option = (option) => {
    if(option == 'New run configuration'){
      $scope.get_templates();
      $scope.modal_trigger('new_run_modal');
    }
  }

  $scope.create_run = (template) => {
    run_name = $('#new_run_name').val();
    if(!run_name || run_name.length == 0){
      $scope.$parent.showToast('New run requires a name');
      return;
    }

    if(template){
      params = {
        'run_name': run_name,
        'template': template
      }
    } else {
      params = {
        'run_name': run_name
      }
    }
    $http({
      url: '/run_manager/create_run/',
      data: params,
      method: 'POST',
      headers: {
        'X-CSRFToken' : $scope.$parent.get_csrf()
      }
    }).then((res) => {
      console.log('created a new run');
      console.log(res.data);
      if('error' in res.data){
        $scope.$parent.showToast(res.data['error']);
      }
      $scope.run_list.push(run_name);
      $('#new_run_modal').closeModal();
      //$scope.$apply();
    }).catch((res) => {
      console.log('Error creating new run');
      console.log(res.data);
      $scope.$parent.showToast('Error creating new run');
    });
  }

  $scope.get_runs = () => {
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
    }).catch((res) => {
      $scope.ready = true;
      console.log('Failed to get runs');
      console.log(res);
    })
  }

  $scope.template_select_options = () => {
    $scope.modal_trigger('copy_template_modal');
    $scope.get_templates();

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

  $scope.modal_trigger = (id) => {
    $('#' + id).openModal();
    $('.modal').css({'bottom': 'inherit'});
  }

  $scope.select_template = (template) => {

  }

  $scope.get_run_data = (run) => {
    $scope.switch_arrow(run);
    if($scope.selected_run != run){
      $scope.selected_run = run;
      $http({
        url: '/run_manager/get_scripts',
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
