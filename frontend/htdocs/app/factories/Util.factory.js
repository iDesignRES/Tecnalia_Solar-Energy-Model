angular.module('UtilFactory', [])
	.factory("utilFactory", function() {
		return {
			clone: function(sourceObject) {
				return JSON.parse(JSON.stringify(sourceObject));
			},
			validateEmail: function(sourceValue) {
				if (/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(sourceValue)) {
    				return true;
				}
				return false;
			},
			getCurrentTimestamp: function() {
				return Math.floor(Date.now() / 1000);
			},
			timestampToFormattedDate: function(sourceTimestamp) {
				if (sourceTimestamp != null) {
					var date = new Date(sourceTimestamp);
					return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
				}
				return null;
			}
		}
	});