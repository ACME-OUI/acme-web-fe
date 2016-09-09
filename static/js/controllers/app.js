(function(){
  var dashboard = angular.module('dashboard', ['data_manager', 'run_manager', 'notification_manager'])
  .controller('DashboardControl', function($scope, $rootScope) {

    $scope.init = () => {
      console.log('[+] Initializing dashboard scope.id = ' + $scope.$id);
      console.log($rootScope);
    }

   //  $scope.showToast = function(message) {
   //    $mdToast.show(
   //      $mdToast.simple()
   //        .textContent(message)
   //        .position('center')
   //        .hideDelay(1200)
   //    );
   //  };

   //  $scope.get_user = () => {
   //    $http({
   //      url: '/run_manager/get_user',
   //      method: 'GET'
   //    }).then((res) => {
   //      $scope.user = res.data
   //    }).catch((res) => {
   //      console.log('Error getting user');
   //      console.log(res);
   //    })
   //  }

   //  $scope.setup_socket = () => {
   //    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
   //    if(!window.ACMEDashboard.socket){
   //      window.ACMEDashboard.socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
   //    }
   //    window.ACMEDashboard.socket.onopen = function() {
   //      message = JSON.stringify({
   //        'target_app': 'run_manager',
   //        'destination': 'init',
   //        'content': 'hello world!'
   //      })
   //      window.ACMEDashboard.socket.send(message);
   //    }
   //    window.ACMEDashboard.socket.onmessage = (message) => {
   //      var data = JSON.parse(message.data);
   //      if(data.user != $scope.user){
   //        return;
   //      }
   //      switch (data.destination) {
   //        case 'set_run_status':
   //          console.log('got a status update');
   //          $scope.set_status_text(data.status, data.job_id + "_queue");
   //          break;
   //        default:

   //      }
   //    }
   //  }

   //  /**
   //   * Slices the object. Note that returns a new spliced object,
   //   * e.g. do not modifies original object. Also note that that sliced elements
   //   * are sorted alphabetically by object property name.
   //   * see: http://stackoverflow.com/a/20682709
   //   */
   //  $scope.slice = (obj, start, end) => {
   //      var sliced = {};
   //      var i = 0;
   //      for (var k in obj) {
   //          if (i >= start && i < end)
   //              sliced[k] = obj[k];
   //          i++;
   //      }
   //      return sliced;
   //  }

   //  $scope.get_csrf = () => {
  	// 	return $('input[name="csrfmiddlewaretoken"]').attr('value');
  	// }

  })
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
