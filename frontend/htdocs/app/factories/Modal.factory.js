angular.module('ModalFactory', [])
	.factory("modalFactory", function($document) {
		return {
			doOpenModalInfo: function(title, message) {
				$('#modalinfo').modal({
					startingTop: '60%',
					dismissible: false,
					inDuration: 450,
					outDuration: 300
				});
				$('#modalinfo').modal('open');
				$('#modalinfo-title').text(title);
				$('#modalinfo-message').html(message);
			},
			doOpenModalConfirm: function(scope, title, message, okFunctionName, okFunctionParameters) {
				$('#modalconfirm').modal({
					startingTop: '60%',
					dismissible: false,
					inDuration: 450,
					outDuration: 300
				});
				$('#modalconfirm').modal('open');
				$('#modalconfirm-title').text(title);
				$('#modalconfirm-message').html(message);
				
				$document[0].getElementById('btnAccept').onclick = function() {
					if (okFunctionParameters != null && okFunctionParameters.length > 0) {
						eval(okFunctionName)(okFunctionParameters);
					} else {
						eval(okFunctionName)();
					}
				};
			}
		}
	});