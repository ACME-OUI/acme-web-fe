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

    $scope.get_notification_list = () => {
      $http({
        url: '/acme/get_notification_list/',
        method: 'GET'
      }).then((res) => {
        $scope.notificaiton_list = res.data;
      }).catch((res) => {
        console.log('error retrieving notification list from server')
      })
    }

    $scope.open_output = (notification) => {
      var text = '';
      $.each(notification.optional_message.text, (i, v) => {
        text += v;
      })
      $('#text_edit_modal').openModal();
      window.ACMEDashboard.ace.setValue(text);
      window.ACMEDashboard.ace.setReadOnly(true);
      $('#text_edit_save_btn').addClass('disabled');
    }

    $scope.setup_socket = () => {
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      if(!window.ACMEDashboard.socket){
        window.ACMEDashboard.socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
      }
      window.ACMEDashboard.notificaiton_list = window.ACMEDashboard.notificaiton_list || [];
      window.ACMEDashboard.socket_handlers = window.ACMEDashboard.socket_handlers || {};
      window.ACMEDashboard.socket_handlers.notification = (data) => {
        $scope.$apply(() => {
          console.log('got a notication');
          console.log(data);
          $scope.notification_list.push(data);
        })
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