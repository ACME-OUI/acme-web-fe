(function(){
  angular.module('notification_manager', ['ngAnimate', 'ngMaterial'])
  .controller('NotificationControl', ['$scope', '$http', '$timeout', '$mdToast', function($scope, $http, $timeout, $mdToast) {
  	$scope.init = () => {
  		console.log('[+] Notification manager init');
  		$scope.notification_list = [];
  	}

  	$scope.$on('notification', (notification) => {
  		$scope.notification_list.push(notification);
  		console.log(notification);
  	})
  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);