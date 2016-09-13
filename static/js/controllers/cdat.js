
angular.module('cdat', [])
.controller('CDATControl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {

  $scope.init = function(){
    console.log('[+] Initializing CDAT window');
  //   $timeout(() => {
  //   	// Point to the element you want to embed the canvas in
		// var canvas = vcs.init("cesiumContainer", "http://aims2.llnl.gov:8008");
		// var f = cdms.open("/export/baldwin32/projects/acme-web-fe/userdata/btest12/model_output/metadiags_test_data/20160520.A_WCYCL1850.ne30_oEC.edison.alpha6_01_ANN_climo.nc", "http://aims2.llnl.gov:8008")
		// var z3 = f.getVariable("Z3");
		// z3.then(function(v){
		// 	canvas.boxfill(v);
		// });
  //   }, 500);
	
  }

}])
