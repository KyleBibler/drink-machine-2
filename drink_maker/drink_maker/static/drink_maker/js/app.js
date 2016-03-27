

// var loadRecipeHtml = function(recipes) {
// 	var html = "";
// 	recipes.forEach(function(recipe) {
// 		html += '<div class="re-recipe-container>"';

// 		html += '</div>';
// 	});
// }

// var getRecipes = function() {
// 	$.ajax({
// 		url: "/recipes/",
// 	    type: "GET",
// 	    success: function(json) {
// 	      	recipes = json["recipes"];

// 	    	loadDrinkMakerHtml(recipes);
// 	    	loadRecipeHtml(recipes);
// 	    }
// 	});
// };

// var getValves = function() {
// 	$.ajax({
// 		url: "/valves/",
// 	    type: "GET",
// 	    success: function(json) {
// 	      	valves = json["valves"];
// 	    }
// 	});
// };

// var getLiquids = function() {
// 	$.ajax({
// 		url: "/liquids/",
// 	    type: "GET",
// 	    success: function(json) {
// 	      	liquids = json["liquids"];
// 	    }
// 	});
// };

// var pollDrinkRequest = function() {
// 	$.ajax({
// 		url: "/drinks/",
// 	    type: "GET",
// 	    success: function(json) {
// 	      	if(json.length > 0) {
// 	      		console.log("There is a request being fulfilled");
// 	      	}
// 	    }
// 	});
// }

// getRecipes();

angular.module('Barkeep', [
	'ngResource'
])

.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
}])

.controller('MainCtrl', ['$scope', 'RestApi', function ($scope, RestApi) {
	$scope.recipes = RestApi.getRecipes();
	$scope.liquids = RestApi.getLiquids();
	$scope.valves = RestApi.getValves();
	$scope.view = {value: 'home'};

	$scope.addingLiquid = false;
	$scope.liquidForm = {};
	$scope.liquidError = {value: false};

	$scope.openAdd = function(isAdding) {
		$scope.addingLiquid = isAdding;
	}

	var showLiquidError = function(errorMsg) {
		$scope.liquidError.value = true;
		setTimeout(function() {
			$scope.liquidError.value = false;
		}, 5000);
	}

	$scope.addLiquid = function(liquid) {
		if(!liquid.name) {
			showLiquidError("Liquid name is required.");
		} else {			
			RestApi.addLiquid(liquid, function() {
				$scope.addingLiquid = false;
				$scope.liquidForm = {};
				$scope.liquids = RestApi.getLiquids();
			});
		}		
	}

	$scope.editLiquid = function(liquid) {
		RestApi.editLiquid(liquid, function() {
			$scope.liquids = RestApi.getLiquids();
		});
	}
}])

.directive('bkLiquid', [function() {
	function link (scope, element, attr) {

	};

	return {
		templateUrl: '/static/drink_maker/partials/bkLiquid.html',
		restrict: 'A',
		scope: {
			liquid: '='
		},
		link: link
	}
}])

.factory('RestApi', ['$resource', function ($resource) {
	var recipeApi = $resource('/recipes/:recipeId', {recipeId: 'recipe_pk'}),
		liquidApi = $resource('/liquids/:liquidId', {liquidId: 'liquid_pk'}),
		valveApi = $resource('/valves/:valveId', {valveId: 'valve_pk'})

	return {
		getRecipes: function () {
			return recipeApi.query();
		},
		getLiquids: function() {
			return liquidApi.query();
		},
		addLiquid: function(liquid, callback) {
			var newLiquid = new liquidApi(liquid);
			newLiquid.$save(callback);
		},
		editLiquid: function(liquid, callback) {
			liquid.$save(callback);
		},
		getValves: function() {
			return valveApi.query();
		}

	};
}]);
