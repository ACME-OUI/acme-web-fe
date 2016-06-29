(function(){
  var dashboard = angular.module('dashboard', ['esgf', 'velo', 'cdat', 'ngAnimate', 'ngMessages', 'ngMaterial'])
  .controller('DashboardControl', ['$scope', '$http', '$mdToast', function($scope, $http, $mdToast) {


    $scope.init = () => {
      console.log('[+] Initializing dashboard');
    }
    

    $scope.addMenuItem = function( title, text ) {
      var element = $( '<li>' + title + '</li>' );
      $( '#menuContainer' ).append( element );

      var newItemConfig = {
          title: title,
          type: 'component',
          componentName: title,
          componentState: { templateId: text }
      };

      layout.createDragSource( element, newItemConfig );
    };


    $scope.showToast = function(message) {
      var pinTo = $scope.getToastPosition();
      $mdToast.show(
        $mdToast.simple()
          .textContent(message)
          .position('center')
          .hideDelay(3000)
      );
    };


    $scope.get_csrf = () => {
  		var nameEQ = "csrftoken=";
  		var ca = document.cookie.split(';');
  		for (var i = 0; i < ca.length; i++) {
  			var c = ca[i];
  			while (c.charAt(0) == ' ') c = c.substring(1, c.length);
  			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
  		}
  		return null;
  	}
  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
