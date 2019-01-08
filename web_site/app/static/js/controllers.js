'use strict';

function IndexController($scope, Crawler, webService) {
	$scope.data = [];
	$scope.submitting = false;
	$scope.showResult = false;

	$scope.crawlerFormSubmit = function() {
		$scope.data = [];
		$scope.minimumProduct = undefined;
		$scope.showResult = false;
		$scope.submitting = true;

		webService.get('/crawler/', { query: $scope.query }).then(function(response) {
			$scope.data = response.data.data;

			// todo: refact
			let min = { price: undefined, item: undefined };
			for (const resource of $scope.data) {
				for (const product of resource.products) {
					if (min.price === undefined || product.price < min.price) {
						min = { price: product.price, item: product };
					}
				}
			}

			$scope.minimumProduct = min.item;
			$scope.submitting = false;
			$scope.showResult = true;
		}, function() {
			console.log('bad');
			$scope.submitting = false;
			$scope.showResult = true;
		});
	};
}

function AboutController($scope) {
	
}
