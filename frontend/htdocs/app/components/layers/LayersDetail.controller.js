idesignresAPP.controller("LayersDetailController", function($scope, $state, $stateParams, $http, $window, $translate, modalFactory, routeFactory, sessionFactory, utilFactory) {
	// Init factories
	$scope.modalFactory = modalFactory;
	$scope.routeFactory = routeFactory;
	$scope.sessionFactory = sessionFactory;
	$scope.utilFactory = utilFactory;
	
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
		});
	};
	
	
	// Function: doValidateLayerFormat
	$scope.doValidateLayerFormat = function(myFile) {
		let myFileExtension = myFile.name.split('.')[1];
		let found = new Array();
		found[0] = false;
		found[1] = false;
		for (let i = 0;i < $scope.layerAllowedFormats.length;i++) {
			if ($scope.layerAllowedFormats[i].extension == myFileExtension) {
				found[0] = true;
				break;
			}
		}
		for (let i = 0;i < $scope.layerObj.formats.length;i++) {
			if (myFileExtension == $scope.layerObj.formats[i].extension && $scope.layerObj.formats[i].uuid == $scope.layerObj.layerFormat) {
				found[1] = true;
				break;
			}
		}
		return found;
	};
	
	
	// Function: doSave
	$scope.doSave = function(myFile) {
		// Upload the file and save
		if (typeof myFile === 'undefined' || myFile == null) {
			$scope.modalFactory.doOpenModalInfo($translate.instant('global.validationError'), $translate.instant('layers.error.noImage'));
		} else {
			// Validate the format
			let formatValidation = $scope.doValidateLayerFormat(myFile);
			if (!formatValidation[0]) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.validationError'), $translate.instant('layers.error.formatError01'));
			} else if(!formatValidation[1]) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.validationError'), $translate.instant('layers.error.formatError02'));
			} else {
				// Add the file to the FormData object
				let formData = new FormData();
				formData.append('file', myFile);
				formData.append('layer', new Blob([JSON.stringify($scope.layerObj)], { type: 'application/json' }));
			
				// Call service
				$scope.ready = false;
				$scope.notReadyText = $translate.instant('layers.wait.save');
				$http({
					method  : 'POST',
					url     : $scope.backendUrl + $scope.apiLayersAdd,
					transformRequest: angular.identity,
					headers : {
						'Content-Type' : undefined,
						'Authorization': 'Bearer ' + $scope.loginObject.token,
						'Accept-language': $scope.loginObject.locale
					},
					data	: formData,
					transformResponse: function (data) {
						return {data: data};
					}
				})
				.success(function(response) {
					$scope.fileObj = null;
					$scope.modalFactory.doOpenModalInfo($translate.instant('global.success'), response.data);
					$scope.routeFactory.goLayers(1);
				})
				.error(function(response, status) {
					$scope.fileObj = null;
					$scope.ready = true;
					$scope.notReadyText = null;
					$scope.errorCode = $translate.instant('global.error').replace('{1}', status);
					if (status == -1 || status == 502) {
						$scope.modalFactory.doOpenModalInfo($scope.errorCode, $translate.instant('global.backendUnavailable'));
					} else {
						$scope.modalFactory.doOpenModalInfo($scope.errorCode, response.data);
					}
				});
			}
		}
	}
	
	
	// Execute when the view content is loaded
	$scope.$on('$viewContentLoaded', function() {
		// Load configuration
		$http.get('/config/config.json').then(function(response) {
			// Define app objects
			$scope.backendUrl = response.data.app.backendUrl;
			$scope.defaultUuid = response.data.app.defaultUuid;
			
			// Define API objects
			$scope.apiLayersUuid = response.data.api.apiLayersUuid;
			$scope.apiLayersAdd = response.data.api.apiLayersAdd;
			
			// Define layers related object
			$scope.layerAllowedFormats = response.data.layers.allowedFormats;
			
			// Define 'layerObj' object
			$scope.layerObj = { uuid:null, name: null, fullPath: null, scale: null, layerFormat: null };
			
			// Define flags
			$scope.ready = true;
			$scope.notReadyText = null;
			$scope.currentPage = $stateParams.currentPage == null ? 1 : $stateParams.currentPage;
			
			// Load the Layer (if necessary)
			if ($stateParams.uuid == null) {
				$scope.routeFactory.goLayers(1);
			}
			$scope.doLoadLayer();
		});
		
		// Update the sidenav
		$scope.sessionFactory.updateUI($scope, $translate);
		
		// Move the scroll to the top of the page
		$window.scrollTo(0, 0);
	});
});