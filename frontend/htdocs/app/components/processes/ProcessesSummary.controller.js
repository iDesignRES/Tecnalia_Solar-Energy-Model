idesignresAPP.controller("ProcessesSummaryController", function($scope, $state, $stateParams, $http, $window, $translate, modalFactory, routeFactory, sessionFactory) {
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
	
	
	// Function: doLoadProcess
	$scope.doLoadProcess = function() {
		// Call service
		$scope.ready = false;
		$scope.notReadyText = $translate.instant('processes.wait.load');
		$http({
			method  : 'GET',
		    url     : $scope.backendUrl + $scope.apiProcessesUuid.replace('{uuid}', $stateParams.uuid),
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
			$scope.processObj = angular.fromJson(response.data);
			if ($scope.processObj == null) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.error404'), $translate.instant('processes.error.noProcess'));
				$scope.routeFactory.goProcesses($scope.currentPage);
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
	
	
	// Function: doDownloadFile
	$scope.doDownloadFile = function(fileName) {
		// Call service
		$scope.ready = false;
		$scope.notReadyText = $translate.instant('processes.wait.download');
		$http({
			method  : 'POST',
		    url     : $scope.backendUrl + $scope.apiProcessesDownload,
		    headers : {
		        'Content-Type' : 'application/json',
		        'Authorization': 'Bearer ' + $scope.loginObject.token,
				'Accept-language': $scope.loginObject.locale
		    },
			data	: $scope.processObj.uuid + '_' + fileName,
		    transformResponse: function (data) {
		        return {data: data};
		    },
		    responseType: 'arraybuffer'
		})
		.success(function(response) {
			$scope.ready = true;
			$scope.notReadyTextText = null;
			let urlCreator = window.URL || window.webkitURL || window.mozURL || window.msURL;
			if (response.data != null && urlCreator) {
				let hiddenElement = document.createElement("a");
				let blob = new Blob([response.data], { type: 'application/zip' });
				let url = urlCreator.createObjectURL(blob);
				hiddenElement.href = url;
				hiddenElement.download = fileName;
				hiddenElement.target = '_blank';
				hiddenElement.style = 'display: none';
				document.body.appendChild(hiddenElement);
				hiddenElement.click();
				setTimeout(function() {window.URL.revokeObjectURL(url), 100});
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
			$scope.apiProcessesUuid = response.data.api.apiProcessesUuid;
			$scope.apiProcessesDownload = response.data.api.apiProcessesDownload;
			
			// Define flags
			$scope.ready = true;
			$scope.notReadyTextText = null;
			$scope.currentPage = $stateParams.currentPage == null ? 1 : $stateParams.currentPage;
			
			// Load the Process
			if ($stateParams.uuid == null) {
				$scope.routeFactory.goProcesses(1);
			} else {
				$scope.doLoadProcess();
			}
		});
		
		// Update the sidenav
		$scope.sessionFactory.updateUI($scope, $translate);
		
		// Move the scroll to the top of the page
		$window.scrollTo(0, 0);
	});
});
