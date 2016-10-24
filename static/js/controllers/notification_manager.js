(function(){
  angular.module('notification_manager', ['ui.ace', 'ngAnimate', 'ngMaterial'])
  .controller('NotificationControl', function($scope, $http, $rootScope) {
    $scope.init = () => {
      console.log('[+] Initializing Notification Manager parent scope.id = ' + $scope.$parent.$id);
      $scope.notification_list = [];
      $scope.get_notification_list();
      $scope.setup_socket();

      // ACE setup
      $scope.aceModel = '';
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
    }

    $scope.get_user = () => {
      $http({
        url: '/run_manager/get_user',
        method: 'GET'
      }).then((res) => {
        window.ACMEDashboard.user = res.data
      }).catch((res) => {
        console.log('Error getting user');
        console.log(res);
      });
    }

    $scope.get_notification_list = () => {
      $http({
        url: '/acme/get_notification_list/',
        method: 'GET'
      }).then((res) => {
        var list = res.data;
        $.each(list, (i, v) => {
          if(v == ' '){
            return;
          }
          var note = JSON.parse(v);
          $scope.list_insert(note);
        });
        $('.collapsible').collapsible({
            accordion : false
          });
      }).catch((res) => {
        console.log('error retrieving notification list from server')
      }).then(() => {
        console.log($scope.notification_list)
      })
    }

    $scope.list_insert = (note) => {
      var inserted = false;
      for(var key in $scope.notification_list){
        let value = $scope.notification_list[key];
        if(value.job_id == note.job_id){
          value.list.push(note);
          inserted = true;
        }
      }
      if(!inserted){
        $scope.notification_list.push({
          'job_id': note.job_id,
          'list': [note]
        });
      }
    }

    $scope.open_output = (notification) => {
      var text = '';
      var params = {
        'run_name': notification.optional_message.run_name,
        'job_id': notification.job_id
      }
      $http({
        url: '/run_manager/get_run_output/',
        method: 'GET',
        params: params
      }).then((res) => {
        text = res.data.output;
        $('#text_edit_modal').openModal();
        window.ACMEDashboard.ace.setValue(text);
        window.ACMEDashboard.ace.setReadOnly(true);
        window.ACMEDashboard.ace.setMode('text');
        $('#text_edit_save_btn').addClass('disabled');
      }).catch((res) => {
        console.log(res);
      });
    }

    $scope.setup_socket = () => {
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      if(!window.ACMEDashboard.socket){
        window.ACMEDashboard.socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
      }
      window.ACMEDashboard.notificaiton_list = window.ACMEDashboard.notificaiton_list || [];
      window.ACMEDashboard.socket_handlers = window.ACMEDashboard.socket_handlers || {};
      window.ACMEDashboard.socket_handlers.notification = (data) => {
        console.log('got a notication');
        console.log(data);
        $scope.$apply(() => {
          $scope.list_insert(data);
        });
      }


      window.ACMEDashboard.socket.onmessage = (message) => {
        $scope.$apply(() => {
          var data = JSON.parse(message.data);
          if(data.user != window.ACMEDashboard.user){
            return;
          }
          for(key in window.ACMEDashboard.socket_handlers){
            if(!window.ACMEDashboard.socket_handlers.hasOwnProperty(key)){
              continue;
            }
            if(key == data.destination){
              console.log(`sending socket command to ${key} with ${data} from notification manager`);
              window.ACMEDashboard.socket_handlers[key](data);
              break;
            }
          }
        });
      }
    }
  })
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);