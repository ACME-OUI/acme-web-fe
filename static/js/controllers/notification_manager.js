(function(){
  angular.module('notification_manager', ['ngAnimate', 'ngMaterial'])
  .controller('NotificationControl', function($scope, $http, $rootScope) {
    $scope.init = () => {
      console.log('[+] Initializing Notification Manager parent scope.id = ' + $scope.$parent.$id);
      $scope.notification_list = [];
      console.log($rootScope);
    }
    $rootScope.$on('notification', (event, notification) => {
      $scope.$apply(() => {
        console.log('got a notification');
        console.log(notification);
        $scope.notification_list.push(notification.message);
      });
    });
  })
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);