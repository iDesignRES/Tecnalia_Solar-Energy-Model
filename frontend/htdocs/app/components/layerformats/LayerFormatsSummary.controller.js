idesignresAPP.controller("LayerFormatsSummaryController", function($scope, $state, $stateParams, $http, $window, $translate, modalFactory, routeFactory, sessionFactory) {
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
	
	
	// Function: doLoadLayerFormat
	$scope.doLoadLayerFormat = function() {
		// Call service
		$scope.ready = false;
		$scope.notReadyText = $translate.instant('layerFormats.wait.load');
		$http({
			method  : 'GET',
		    url     : $scope.backendUrl + $scope.apiLayerFormatsUuid.replace('{uuid}', $stateParams.uuid),
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
			$scope.layerFormatObj = angular.fromJson(response.data);
			if ($scope.layerFormatObj == null) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.error404'), $translate.instant('layerFormats.error.noLayerFormat'));
				$scope.routeFactory.goLayerFormats($scope.currentPage);
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
			$scope.apiLayerFormatsUuid = response.data.api.apiLayerFormatsUuid;
			
			// Define flags
			$scope.ready = true;
			$scope.notReadyTextText = null;
			$scope.currentPage = $stateParams.currentPage == null ? 1 : $stateParams.currentPage;
			
			// Load the Layer Format
			if ($stateParams.uuid == null) {
				$scope.routeFactory.goLayerFormats(1);
			} else {
				$scope.doLoadLayerFormat();
			}
		});
		
		// Update the sidenav
		$scope.sessionFactory.updateUI($scope, $translate);
		
		// Move the scroll to the top of the page
		$window.scrollTo(0, 0);
	});
});