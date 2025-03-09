var idesignresAPP = angular.module('idesignresAPP', ['ui.router', 'ModalFactory', 'RouteFactory', 'SessionFactory', 'UtilFactory', 'pascalprecht.translate', 'angular-jwt']);

idesignresAPP.config(function($stateProvider, $urlRouterProvider, $translateProvider, $translatePartialLoaderProvider) {
	
	// I18N
	$translateProvider.useLoader('$translatePartialLoader', {
		urlTemplate: '/i18n/{lang}/{part}.json'
	})
	.preferredLanguage('en')
	.useSanitizeValueStrategy('escape');
	
	// States
    $stateProvider.state('/', {
        url: '/',
        controller:'LoginController',
        templateUrl:'app/components/login/login.html',
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('login');
				return $translate.refresh();
			}]
		}
    })
    .state('roles', {
        url: '/roles',
        controller: 'RolesController',
        templateUrl:'app/components/roles/roles.html',
        data: {
        	authorities: ['ROLE_ADMINISTRATOR']
        },
        params: { currentPage: null },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('roles');
				return $translate.refresh();
			}]
		}
    })
    .state('roles-summary', {
        url: '/roles-summary',
        controller:'RolesSummaryController',
        templateUrl:'app/components/roles/rolessummary.html',
        params: { uuid: null, currentPage: null },
        data: {
        	authorities: ['ROLE_ADMINISTRATOR']
        },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('roles');
				return $translate.refresh();
			}]
		}
    })
    .state('users', {
        url: '/users',
        controller:'UsersController',
        templateUrl:'app/components/users/users.html',
        data: {
        	authorities: ['ROLE_ADMINISTRATOR']
        },
        params: { currentPage: null },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('users');
				return $translate.refresh();
			}]
		}
    })
    .state('users-detail', {
        url: '/users-detail',
        controller:'UsersDetailController',
        templateUrl:'app/components/users/usersdetail.html',
        params: { uuid: null, currentPage: null },
        data: {
        	authorities: ['ROLE_ADMINISTRATOR']
        },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('users');
				return $translate.refresh();
			}]
		}
    })
    .state('users-summary', {
        url: '/users-summary',
        controller:'UsersSummaryController',
        templateUrl:'app/components/users/userssummary.html',
        params: { uuid: null, currentPage: null },
        data: {
        	authorities: ['ROLE_ADMINISTRATOR']
        },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('users');
				return $translate.refresh();
			}]
		}
    })
	.state('scales', {
	    url: '/scales',
		controller: 'ScalesController',
		templateUrl:'app/components/scales/scales.html',
		data: {
		   	authorities: ['ROLE_ADMINISTRATOR']
		},
		params: { currentPage: null },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('scales');
				return $translate.refresh();
			}]
		}
	})
	.state('scales-summary', {
	    url: '/scales-summary',
	    controller:'ScalesSummaryController',
	    templateUrl:'app/components/scales/scalessummary.html',
	    params: { uuid: null, currentPage: null },
	    data: {
	      	authorities: ['ROLE_ADMINISTRATOR']
	    },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('scales');
				return $translate.refresh();
			}]
		}
	})
	.state('processes', {
        url: '/processes',
	    controller: 'ProcessesController',
	    templateUrl:'app/components/processes/processes.html',
	    data: {
	     	authorities: ['ROLE_ADMINISTRATOR', 'ROLE_OPERATOR']
	    },
	    params: { currentPage: null },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('processes');
				return $translate.refresh();
			}]
		}
	})
	.state('processes-summary', {
	    url: '/processes-summary',
	    controller:'ProcessesSummaryController',
	    templateUrl:'app/components/processes/processessummary.html',
	    params: { uuid: null, currentPage: null },
	    data: {
	      	authorities: ['ROLE_ADMINISTRATOR', 'ROLE_OPERATOR']
	    },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('processes');
				return $translate.refresh();
			}]
		}
	})
	.state('layer-formats', {
        url: '/layer-formats',
	    controller: 'LayerFormatsController',
	    templateUrl:'app/components/layerformats/layerformats.html',
	    data: {
	     	authorities: ['ROLE_ADMINISTRATOR']
	    },
	    params: { currentPage: null },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('layerformats');
				return $translate.refresh();
			}]
		}
	})
	.state('layer-formats-summary', {
	    url: '/layer-formats-summary',
	    controller:'LayerFormatsSummaryController',
	    templateUrl:'app/components/layerformats/layerformatssummary.html',
	    params: { uuid: null, currentPage: null },
	    data: {
	      	authorities: ['ROLE_ADMINISTRATOR']
	    },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('layerformats');
				return $translate.refresh();
			}]
		}
	})
	.state('layers', {
	    url: '/layers',
	    controller: 'LayersController',
		templateUrl:'app/components/layers/layers.html',
		data: {
		   	authorities: ['ROLE_ADMINISTRATOR']
		},
		params: { currentPage: null },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('layers');
				return $translate.refresh();
			}]
		}
	})
	.state('layers-detail', {
		url: '/layers-detail',
		controller:'LayersDetailController',
		templateUrl:'app/components/layers/layersdetail.html',
		params: { uuid: null, currentPage: null },
		data: {
			authorities: ['ROLE_ADMINISTRATOR']
		},
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('layers');
				return $translate.refresh();
			}]
		}
    })
	.state('layers-summary', {
	    url: '/layers-summary',
	    controller:'LayersSummaryController',
	    templateUrl:'app/components/layers/layerssummary.html',
	    params: { uuid: null, currentPage: null },
	    data: {
	      	authorities: ['ROLE_ADMINISTRATOR']
	    },
		resolve: {
			translatePartialLoader: ['$translate', '$translatePartialLoader', function($translate, $translatePartialLoader) {
				$translatePartialLoader.addPart('global');
				$translatePartialLoader.addPart('layers');
				return $translate.refresh();
			}]
		}
	});

    $urlRouterProvider.otherwise('/');
});