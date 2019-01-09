'use strict';

angular.module('appServices', ['ngResource'])
	.factory('Post', function($resource) {
		return $resource('/api/post/:postId', {}, {
			query: {
				method: 'GET',
				params: { postId: '' },
				isArray: true
			}
		});
	})
	.factory('Crawler', function($resource) {
		return $resource('/crawler/', {}, {
			query: {
				method: 'GET',
				params: { postId: '12' }
			}
		});
	});

angular.module('appServices').service('webService', function($http) {
	this.get = function (url, data) {
		return $http.get(url, { params: data })
	};

	this.delete = function (url, data) {
		return $http.delete(url, { params: data })
	};

	this.post = function (url, data) {
		return $http.post(url, data)
	};
});