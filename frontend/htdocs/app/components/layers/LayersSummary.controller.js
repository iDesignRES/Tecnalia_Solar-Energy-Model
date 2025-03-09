idesignresAPP.controller("LayersSummaryController", function($scope, $state, $stateParams, $http, $window, $translate, modalFactory, routeFactory, sessionFactory) {
	// Init factories
	$scope.modalFactory = modalFactory;
	$scope.routeFactory = routeFactory;
	$scope.sessionFactory = sessionFactory;
	
	// Check session
	$scope.loginObject = angular.fromJson($window.sessionStorage.getItem('loginObject'));
	$scope.sessionFactory.checkSession($scope.loginObject);
	
	// Check permissions
	if (!$scope.sessionFactory.hasPermissions($scope.loginObject, $state.current.data.authorities)) {
		$scope.modalFactory.doOpenModalInfo($translate.instant('global.error403'), $translate.instant('global.unauthorized'));
		$scope.routeFactory.doLogout();
	}
	
	
	// Function: doLoadLayer
	$scope.doLoadLayer = function() {
		// Call service
		$scope.ready = false;
		$scope.notReadyText = $translate.instant('layers.wait.load');
		$http({
			method  : 'GET',
		    url     : $scope.backendUrl + $scope.apiLayersUuid.replace('{uuid}', $stateParams.uuid),
		    headers : {
		        'Content-Type' : 'application/json',
		        'Authorization': 'Bearer ' + $scope.loginObject.token,
				'Accept-language': $scope.loginObject.locale
		    },
			data	: {},
		    transformResponse: function (data) {
		        return {data: data};
		    }
		})
		.success(function(response) {
			$scope.ready = true;
			$scope.notReadyTextText = null;
			$scope.layerObj = angular.fromJson(response.data);
			if ($scope.layerObj == null) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.error404'), $translate.instant('layers.error.noLayer'));
				$scope.routeFactory.goLayers($scope.currentPage);
			}
		})
		.error(function(response, status) {
			$scope.ready = true;
			$scope.notReadyTextText = null;
			$scope.errorCode = $translate.instant('global.error').replace('{1}', status);
			if (status == -1 || status == 502) {
				$scope.modalFactory.doOpenModalInfo($scope.errorCode, $translate.instant('global.backendUnavailable'));
			} else {
				$scope.modalFactory.doOpenModalInfo($scope.errorCode, response.data);
			}
		});
	};
	
	
	// Execute when the view content is loaded
	$scope.$on('$viewContentLoaded', function() {
		// Load configuration
		$http.get('/config/config.json').then(function(response) {
			// Define app objects
			$scope.backendUrl = response.data.app.backendUrl;
			
			// Define API objects
			$scope.apiLayersUuid = response.data.api.apiLayersUuid;
			
			// Define flags
			$scope.ready = true;
			$scope.notReadyTextText = null;
			$scope.currentPage = $stateParams.currentPage == null ? 1 : $stateParams.currentPage;
			
			// Load the Layer
			if ($stateParams.uuid == null) {
				$scope.routeFactory.goLayers(1);
			} else {
				$scope.doLoadLayer();
			}
		});
		
		// Update the sidenav
		$scope.sessionFactory.updateUI($scope, $translate);
		
		// Move the scroll to the top of the page
		$window.scrollTo(0, 0);
	});
});