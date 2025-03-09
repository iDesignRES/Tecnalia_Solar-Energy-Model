angular.module('RouteFactory', [])
	.factory('routeFactory', function($document, $state) {
		return {
			goRoles: function(currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('roles', { currentPage: currentPage }, { reload: true });
			},
			goRolesSummary: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('roles-summary', { uuid: uuid, currentPage: currentPage });
			},
			goUsers: function(currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('users', { currentPage: currentPage }, { reload: true });
			},
			goUsersDetail: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('users-detail', { uuid: uuid, currentPage: currentPage });
			},
			goUsersSummary: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('users-summary', { uuid: uuid, currentPage: currentPage });
			},
			goScales: function(currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('scales', { currentPage: currentPage }, { reload: true });
			},
			goScalesSummary: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('scales-summary', { uuid: uuid, currentPage: currentPage });
			},
			goProcesses: function(currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('processes', { currentPage: currentPage }, { reload: true });
			},
			goProcessesAssign: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('processes-assign', { uuid: uuid, currentPage: currentPage });
			},
			goProcessesSummary: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('processes-summary', { uuid: uuid, currentPage: currentPage });
			},
			goLayerFormats: function(currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('layer-formats', { currentPage: currentPage }, { reload: true });
			},
			goLayerFormatsSummary: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('layer-formats-summary', { uuid: uuid, currentPage: currentPage });
			},
			goLayers: function(currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('layers', { currentPage: currentPage }, { reload: true });
			},
			goLayersDetail: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('layers-detail', { uuid: uuid, currentPage: currentPage });
			},
			goLayersSummary: function(uuid, currentPage) {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('layers-summary', { uuid: uuid, currentPage: currentPage });
			},
			refreshState: function() {
				$state.reload();
			},
			doLogout: function() {
				M.Sidenav.getInstance($document[0].querySelector('.sidenav')).close();
				$state.go('/');
			}
		}
	});