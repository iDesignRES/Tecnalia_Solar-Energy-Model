idesignresAPP.controller("UsersDetailController", function($scope, $state, $stateParams, $http, $window, $translate, modalFactory, routeFactory, sessionFactory, utilFactory) {
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
	
	
	// Function: doValidate()
	$scope.doValidate = function() {
		if (!$scope.utilFactory.validateEmail($scope.userObj.email)) {
			$scope.modalFactory.doOpenModalInfo($translate.instant('global.validationError'), $translate.instant('global.invalidField').replace('{1}', $translate.instant('users.form.email')));
			return false;
		}
		if ($scope.userObj.password != $scope.userObj.repeatPassword) {
			$scope.modalFactory.doOpenModalInfo($translate.instant('global.validationError'), $translate.instant('users.error.differentPasswords'));
			return false;
		}
		
		return true;
	};
	
	
	// Function: doSave
	$scope.doSave = function() {
		if ($scope.doValidate()) {
			// Call service
			$scope.ready = false;
			$scope.notReadyText = $translate.instant('users.wait.save');
			$http({
				method  : 'POST',
				url     : $scope.backendUrl + $scope.apiUsersAdd,
				headers : {
					'Content-Type' : 'application/json',
					'Authorization': 'Bearer ' + $scope.loginObject.token,
					'Accept-language': $scope.loginObject.locale
				},
				data	: $scope.userObj,
				transformResponse: function (data) {
					return {data: data};
				}
			})
			.success(function(response) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.success'), response.data);
				$scope.routeFactory.goUsers(1);
			})
			.error(function(response, status) {
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
	};
	
	
	// Execute when the view content is loaded
	$scope.$on('$viewContentLoaded', function() {
		// Load configuration
		$http.get('/config/config.json').then(function(response) {
			// Define app objects
			$scope.backendUrl = response.data.app.backendUrl;
			$scope.defaultUuid = response.data.app.defaultUuid;
			
			// Define API objects
			$scope.apiUsersUuid = response.data.api.apiUsersUuid;
			$scope.apiUsersAdd = response.data.api.apiUsersAdd;
			
			// Define 'userObj' object
			$scope.userObj = { username: null, password: null, email: null, uuid: null, role: null, repeatPassword: null, previousUsername: null };
			
			// Define flags
			$scope.ready = true;
			$scope.notReadyText = null;
			$scope.currentPage = $stateParams.currentPage == null ? 1 : $stateParams.currentPage;
			
			// Load the User (if necessary)
			if ($stateParams.uuid == null) {
				$scope.routeFactory.goUsers(1);
			}
		});
		
		// Update the sidenav
		$scope.sessionFactory.updateUI($scope, $translate);
		
		// Move the scroll to the top of the page
		$window.scrollTo(0, 0);
	});
});