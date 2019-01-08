'use strict';

angular.module('appFilters').filter('uppercase', function() {
	return function(input) {
		return input.toUpperCase();
	}
});