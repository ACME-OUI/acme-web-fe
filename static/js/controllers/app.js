(function(){
  var dashboard = angular.module('dashboard', ['ngAnimate', 'ngMessages', 'ngMaterial', 'ngRoute'])
  .controller('DashboardControl', ['$scope', '$http', '$mdToast', function($scope, $http, $mdToast) {

    $scope.init = () => {
      console.log('[+] Initializing dashboard');
      var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
      var chat_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
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
        $scope.user = res.data
      }).catch((res) => {
        console.log('Error getting user');
        console.log(res);
      })
    }

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

    $scope.get_csrf = () => {
  		return $('input[name="csrfmiddlewaretoken"]').attr('value');
  	}

  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
