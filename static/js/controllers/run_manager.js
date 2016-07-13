
angular.module('run_manager', [])
.controller('RunManagerControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing RunManager window');
    $scope.run_options = ['New run configuration', 'start run', 'stop run', 'run status', 'new template'];
    $scope.ready = false;
    $scope.run_list = [];
    $scope.selected_run = undefined;
    $scope.script_list = undefined;
    $scope.template_list = undefined;
    $scope.get_runs();
    $scope.get_templates();
  }

  $scope.trigger_option = (option) => {
    if(option == 'New run configuration'){
      $scope.get_templates();
      $scope.modal_trigger('new_run_modal');
    } else if (option == 'start run') {
      $scope.modal_trigger('start_run_modal');
    }  else if (option == 'stop run') {
      $scope.modal_trigger('stop_run_modal');
    } else if (option == 'run status') {
      $scope.modal_trigger('run_status_modal');
    } else if (option == 'new template') {
      $scope.template_select_options();
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
      $('#new_run_name').val('');
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

  $scope.create_new_template_edit = () => {

  }

  $scope.modal_trigger = (id) => {
    $('#' + id).openModal();
    $('.modal').css({'bottom': 'inherit'});
  }

  $scope.select_template = (template) => {
    var new_template_name = $('#new_template_name').val();
    if(!new_template_name || new_template_name.length == 0){
      $scope.$parent.showToast('Copy template requires a name');
      return;
    }
    $http({
      url: '/run_manager/copy_template/',
      method: 'POST',
      headers: {
        'X-CSRFToken' : $scope.$parent.get_csrf()
      },
      data: {
        template: template,
        new_template: new_template_name
      }
    }).then((res) => {
      console.log('successfully copied template');
      $('copy_template_modal').closeModal();
      $('#new_template_name').val('');
      $scope.$parent.showToast('Successfully copied template');
    }).catch((res) => {
      console.log('Error copying template');
      $scope.$parent.showToast('Error copying template');
    });
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

  $scope.switch_arrow = (id) => {
    var el = $('#'+ id +'_arrow');
    if(el.text() == 'play_arrow'){
      $('#'+ id +'_arrow').text('arrow_drop_down');
    } else {
      $('#'+ id +'_arrow').text('play_arrow');
    }
  }

}]);
