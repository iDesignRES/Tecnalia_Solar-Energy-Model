idesignresAPP.controller("UsersController", function($scope, $state, $stateParams, $http, $window, $translate, modalFactory, routeFactory, sessionFactory) {
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
	

	// Function: doLoadUsers
	$scope.doLoadUsers = function() {
		// Call service
		$scope.ready = false;
		$scope.notReadyText = $translate.instant('users.wait.loadAll');
		$http({
			method  : 'GET',
		    url     : $scope.backendUrl + $scope.apiUsers,
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
			$scope.notReadyText = null;
			$scope.users = angular.fromJson(response.data);
			if ($scope.users == null || $scope.users.length == 0) {
				$scope.modalFactory.doOpenModalInfo($translate.instant('global.error404'), $translate.instant('users.error.noUsers'));
			} else {
				// Pagination settings
				$scope.numberOfPages = Math.ceil($scope.users.length / $scope.itemsPerPage);
				for (var i = 1;i <= $scope.numberOfPages;i++) {
					$scope.pageRange.push(i);
				}
				$scope.$watch('currentPage + itemsPerPage', function() {
					var begin = (($scope.currentPage - 1) * $scope.itemsPerPage),
					end = begin + $scope.itemsPerPage;
					$scope.filteredUsers = $scope.users.slice(begin, end);
				});
			}
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
	};
	
	
	// Function: doAskRemove
	$scope.doAskRemove = function(user) {
		$scope.paramArray = [user];
		$scope.modalFactory.doOpenModalConfirm($scope, $translate.instant('global.confirm'), $translate.instant('users.removeConfirmation'), 'scope.doRemove', $scope.paramArray);
	};
	
	
	// Function: doRemove
	$scope.doRemove = function(callbackParameters) {
		// Call service
		$scope.ready = false;
		$scope.notReadyText = $translate.instant('users.wait.remove');
		$http({
			method  : 'POST',
			url     : $scope.backendUrl + $scope.apiUsersDelete,
			headers : {
				'Content-Type' : 'application/json',
				'Authorization': 'Bearer ' + $scope.loginObject.token,
				'Accept-language': $scope.loginObject.locale
			},
			data	: callbackParameters[0],
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
	};
	
	
	// Execute when the view content is loaded
	$scope.$on('$viewContentLoaded', function() {
		// Load configuration
		$http.get('/config/config.json').then(function(response) {
			// Define app objects
			$scope.backendUrl = response.data.app.backendUrl;
			$scope.defaultUuid = response.data.app.defaultUuid;
			
			// Define API objects
			$scope.apiUsers = response.data.api.apiUsers;
			$scope.apiUsersDelete = response.data.api.apiUsersDelete;
			
			// Define flags
			$scope.ready = true;
			$scope.notReadyText = null;
			
			// Define the pagination parameters
			$scope.currentPage = $stateParams.currentPage == null ? 1 : $stateParams.currentPage;
			$scope.itemsPerPage = response.data.pagination.itemsPerPage;
			$scope.numberOfPages = 1;
			$scope.pageRange = [];
			
			// Load the Users
			$scope.doLoadUsers();
		});
		
		// Update the sidenav
		$scope.sessionFactory.updateUI($scope, $translate);
		
		// Move the scroll to the top of the page
		$window.scrollTo(0, 0);
	});
});