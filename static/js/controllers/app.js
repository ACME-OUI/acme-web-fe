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
      $mdToast.show(
        $mdToast.simple()
          .textContent(message)
          .position('center')
          .hideDelay(1200)
      );
    };

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
