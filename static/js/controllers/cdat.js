
angular.module('cdat', [])
.controller('CDATControl', ['$scope', '$http', function($scope, $http) {

  $scope.init = function(){
    console.log('[+] Initializing CDAT window');
  }

  $scope.new_plot = function new_plot(id, plotvars) {
		console.log("making cdat window");

		var elem = $('#' + id + " .plot-content");
		elem.append(cdat.make_plot_panel());
		if (plotvars && typeof plotvars !== "undefined") {
			elem.find(".cdat-graphic-method").text(plotvars.method);
			elem.find(".cdat-graphic-template").text(plotvars.template);
		}
	}
}])
