angular.module('SessionFactory', [])
	.factory("sessionFactory", function($window, $document, $compile, routeFactory) {
		return {
			cleanSession: function() {
				$window.sessionStorage.removeItem('loginObject');
			},
			checkSession: function(loginObject) {
				if (loginObject == null || loginObject.token == null || loginObject.username == null
					|| loginObject.email == null || loginObject.uuid == null || loginObject.role == null
					|| loginObject.roleList == null || loginObject.roleList.length == 0) {
					   routeFactory.doLogout();
				}
			},
			hasPermissions: function(loginObject, roles) {
				if (loginObject.role == null || roles == null || roles.length == 0) {
					return false;
				} else {
					for (var i = 0;i < roles.length;i++) {
						if (loginObject.role.indexOf(roles[i]) != -1) {
							return true;
						}
					}
					return false;
				}
			},
			renderSelectComponent: function() {
				$(document).ready(function() {
					$('select').formSelect();
				});
			},
			renderTooltipComponent: function() {
				$(document).ready(function() {
					$('.tooltipped').tooltip({
						exitDelay: 0,
						inDuration: 200,
						outDuration: 200,
						margin: 4,
						transitionMovement: 8
					});
					$('.tooltipped').mousedown(function(){
						$('.material-tooltip').css("visibility", "hidden");
					});
					$('.tooltipped').mouseleave(function(){
						$('.material-tooltip').css("visibility", "hidden");
					});
				});
			},
			renderRangeComponent: function() {
				$(document).ready(function() {
					var elems = $document[0].querySelectorAll("input[type=range]");
					M.Range.init(elems);
				});
			},
			updateUI: function(scope, translate) {
				angular.element($document[0].querySelector('#sidenav_username')).html(scope.loginObject.username);
				angular.element($document[0].querySelector('#sidenav_role')).html(scope.loginObject.role);
				
				angular.element($document[0].querySelector('#sidenav_administration')).html(translate.instant('global.sidenav.administration'));
				angular.element($document[0].querySelector('#sidenav_operator')).html(translate.instant('global.sidenav.operator'));
				
				angular.element($document[0].querySelector('#sidenav_roles')).html('<i class="material-icons">streetview</i>' + translate.instant('global.sidenav.roles') + '</i>');
				angular.element($document[0].querySelector('#sidenav_roles')).attr('ng-click', 'routeFactory.goRoles(1)');
				$compile(angular.element($document[0].querySelector('#sidenav_roles')))(scope);
					
				angular.element($document[0].querySelector('#sidenav_users')).html('<i class="material-icons">account_box</i>' + translate.instant('global.sidenav.users') + '</i>');
				angular.element($document[0].querySelector('#sidenav_users')).attr('ng-click', 'routeFactory.goUsers(1)');
				$compile(angular.element($document[0].querySelector('#sidenav_users')))(scope);
				
				angular.element($document[0].querySelector('#sidenav_scales')).html('<i class="material-icons">aspect_ratio</i>' + translate.instant('global.sidenav.scales') + '</i>');
				angular.element($document[0].querySelector('#sidenav_scales')).attr('ng-click', 'routeFactory.goScales(1)');
				$compile(angular.element($document[0].querySelector('#sidenav_scales')))(scope);
				
				angular.element($document[0].querySelector('#sidenav_processes')).html('<i class="material-icons">memory</i>' + translate.instant('global.sidenav.processes') + '</i>');
				angular.element($document[0].querySelector('#sidenav_processes')).attr('ng-click', 'routeFactory.goProcesses(1)');
				$compile(angular.element($document[0].querySelector('#sidenav_processes')))(scope);
				
				angular.element($document[0].querySelector('#sidenav_layerformats')).html('<i class="material-icons">collections_bookmark</i>' + translate.instant('global.sidenav.layerFormats') + '</i>');
				angular.element($document[0].querySelector('#sidenav_layerformats')).attr('ng-click', 'routeFactory.goLayerFormats(1)');
				$compile(angular.element($document[0].querySelector('#sidenav_layerformats')))(scope);
				
				angular.element($document[0].querySelector('#sidenav_layers')).html('<i class="material-icons">collections</i>' + translate.instant('global.sidenav.layers') + '</i>');
				angular.element($document[0].querySelector('#sidenav_layers')).attr('ng-click', 'routeFactory.goLayers(1)');
				$compile(angular.element($document[0].querySelector('#sidenav_layers')))(scope);
				
				// Visibility
				angular.element($document[0].querySelector('#sidenav_processes')).attr('style', 'display: block');
				if (scope.loginObject.role == scope.loginObject.roleList[0]) {
					angular.element($document[0].querySelector('#sidenav_administration')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_roles')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_users')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_scales')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_layerformats')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_layers')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_divider03')).attr('style', 'display: block');
					angular.element($document[0].querySelector('#sidenav_divider04')).attr('style', 'display: block');
									
					angular.element($document[0].querySelector('#sidenav_operator')).attr('style', 'display: none');
				} else {
					angular.element($document[0].querySelector('#sidenav_operator')).attr('style', 'display: block');
					
					angular.element($document[0].querySelector('#sidenav_administration')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_roles')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_users')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_scales')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_layerformats')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_layers')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_divider03')).attr('style', 'display: none');
					angular.element($document[0].querySelector('#sidenav_divider04')).attr('style', 'display: none');
				}
			}
		}
	});