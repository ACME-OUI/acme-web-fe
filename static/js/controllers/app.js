(function(){
  var dashboard = angular.module('dashboard', ['esgf', 'run_manager', 'cdat', 'ngAnimate', 'ngMessages', 'ngMaterial'])
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
  		return $('input[name="csrfmiddlewaretoken"]').attr('value');
  	}

  }])
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    return $interpolateProvider.endSymbol(']]');
  });
}).call(this);
