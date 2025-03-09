idesignresAPP.controller("LoginController", function($scope, $http, $window, $translate, modalFactory, routeFactory, sessionFactory, jwtHelper) {
	// Init factories
	$scope.modalFactory = modalFactory;
	$scope.routeFactory = routeFactory;
	$scope.sessionFactory = sessionFactory;
	
	// Clean session
	$scope.sessionFactory.cleanSession();
	
	
	// Function: doLogin
	$scope.doLogin = function() {
		// Call service
		$scope.ready = false;
		$http({
			method  : 'POST',
			url     : $scope.backendUrl + $scope.apiHelloAuthenticate,
			headers : {
				'Content-Type' : 'application/json',
				'Accept-language': $scope.defaultLocale
			},
			data	: $scope.loginObj,
			transformResponse: function (data) {
				return {data: data};
			}
		})
		.success(function(response) {
			$scope.ready = true;
			$scope.response = angular.fromJson(response.data);
			let decodedToken = jwtHelper.decodeToken($scope.response.token);

			$scope.loginObject = { locale: $scope.defaultLocale, token: $scope.response.token, username: decodedToken.sub, email: decodedToken.email, uuid: decodedToken.identifier, role: decodedToken.role, roleList: new Array() };
			$scope.loginObject.roleList.push($scope.roleAdministrator);
			$scope.loginObject.roleList.push($scope.roleOperator);

			// Store data in session object
			$window.sessionStorage.setItem('loginObject', JSON.stringify($scope.loginObject));
			
			// Redirect taking into account the role
			if ($scope.loginObject.role == $scope.roleAdministrator || $scope.loginObject.role == $scope.roleOperator) {
				$scope.routeFactory.goProcesses(1);
			} else {
				$scope.routeFactory.doLogout();
			}
		})
		.error(function(response, status) {
			$scope.ready = true;
			$scope.login = { user: null, password: null };
			$scope.errorCode = $translate.instant('global.error').replace('{1}', status);
			if (status == -1 || status == 502) {
				$scope.modalFactory.doOpenModalInfo($scope.errorCode, $translate.instant('global.backendUnavailable'));
			} else {
				$scope.modalFactory.doOpenModalInfo($scope.errorCode, response.data);
			}
		});
	};
	
	
	// Function: Capture the ENTER key pressed event
	$scope.enter = function(keyEvent) {
		if (keyEvent.which === 13) {
			$scope.doLogin();
		}
	};
	
	
	// Execute when the view content is loaded
	$scope.$on('$viewContentLoaded', function() {
		// Load configuration
		$http.get('/config/config.json').then(function(response) {
			// Define app objects
			$scope.backendUrl = response.data.app.backendUrl;
			$scope.defaultLocale = response.data.app.defaultLocale;
			
			// Define API objects
			$scope.apiHelloAuthenticate = response.data.api.apiHelloAuthenticate;
			
			// Define role objects
			$scope.roleAdministrator = response.data.roles.administrator;
			$scope.roleOperator = response.data.roles.operator;
			
			// Define loginObj object
			//$scope.loginObj = { username: null, password: null };
			$scope.loginObj = { username: 'operator', password: 'PWDoperator#2024' };
			
			// Define flags
			$scope.ready = true;
		});
	});
});
