angular.module('Barkeep', [
	'ngResource'
])

.config(['$httpProvider', '$resourceProvider', function($httpProvider, $resourceProvider) {
    // $httpProvider.defaults.headers.post['X-CSRFToken'] = $.cookie('csrftoken');
    $httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
    $httpProvider.defaults.headers['delete'] = {
    	'Content-Type': "application/json;charset=utf-8",
		'X-CSRFToken': csrftoken
	};
    $resourceProvider.defaults.stripTrailingSlashes = false;;
}])

.controller('MainCtrl', ['$scope', 'RestApi', function ($scope, RestApi) {
	$scope.recipes = RestApi.getRecipes();
	$scope.liquids = RestApi.getLiquids();
	$scope.valves = RestApi.getValves();
	$scope.view = {value: 'home'};
	$scope.title = "Make a Drink";
	$scope.addingLiquid = false;
	$scope.liquidForm = {};
	$scope.liquidError = {value: false};

	$scope.changeView = function (view) {
		$scope.view.value = view;
		switch (view) {
			case 'home': 
				$scope.title = "Make a Drink";
				break;
			case 'recipe':
				$scope.title = "Recipes";
				break;
			case 'liquid':
				$scope.title = "Liquids";
				break;
			case 'valve': 
				$scope.title = "Valve Config";
				break;
		}
	}

	$scope.addRecipe = function () {
		$scope.recipes.unshift(RestApi.newRecipe());
	};

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

.directive('bkRecipe', ['RestApi', function (RestApi) {
	function link (scope, element, attr) {
		scope.state = scope.recipe.pk != undefined ? 'display' : 'editing';
		scope.deleteRecipe = function (recipe) {
			RestApi.deleteRecipe(recipe, function () {
				scope.recipes.splice(scope.recipes.indexOf(scope.recipe), 1);
			});
		};

		scope.edit = function () {
			scope.state = scope.state == 'editing' ? 'display' : 'editing';
		};

		scope.filterLiquids = function (hash) {
			return !scope.recipe.components.some(function (e) {
				return e.name == hash.name;
			});
		};

		scope.addLiquid = function (liquid) {
			if (liquid) {
				scope.recipe.components.push({
					name: liquid.name,
					volume: 45,
					pk: liquid.pk
				});
				scope.currentLiquid = '';
			}
		}

		scope.removeLiquid = function (liquid) {
			scope.recipe.components.splice(scope.recipe.components.indexOf(liquid), 1)
		};

		scope.saveRecipe = function (recipe) {
			RestApi.saveRecipe(recipe, function () {
				scope.state = 'display';
			});
		};

		scope.cancelSave = function () {
			if (scope.recipe.pk == undefined) {
				scope.recipes.splice(scope.recipes.indexOf(scope.recipe), 1);
			} else {
				scope.recipe = RestApi.getRecipe(scope.recipe.pk);
			}
			scope.state = 'display';
		};

	}

	return {
		templateUrl: '/static/drink_maker/partials/bkRecipe.html',
		restrict: 'A',
		scope: {
			recipe: '=',
			liquids: '=',
			recipes: '='
		},
		link: link
	};
}])

.directive('bkLiquidValve', ['RestApi', function (RestApi) {
	function link (scope, element, attr) {
		scope.state = 'display';

		scope.edit = function () {
			scope.state = scope.state == 'editing' ? 'display' : 'editing';
			if (scope.state == 'display') {
				scope.recipe = RestApi.getValve(scope.recipe.pk);
			}
		}

		// scope.filterLiquids = function (hash) {
		// 	return !scope.recipe.components.some(function (e) {
		// 		return e.name == hash.name;
		// 	});
		// };

		scope.saveValve = function () {
			RestApi.saveRecipe(scope.valve, function () {
				scope.state = 'display';
			});
		}

	}

	return {
		templateUrl: '/static/drink_maker/partials/bkLiquidValve.html',
		restrict: 'A',
		scope: {
			liquids: '=',
			valve: '='
		},
		link: link
	};
}])



.directive('bkLiquid', ['RestApi', function(RestApi) {
	function link (scope, element, attr) {
		scope.editing = {value: false}
		scope.enableEdit = function(editing) {
			scope.editing.value = editing;
		}
		scope.saveEdit = function() {
			RestApi.editLiquid(scope.liquid, function() {
				scope.editing.value = false;
			});
		}

		scope.valves = RestApi.getValves();
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
	var recipeApi = $resource('/recipes/:recipeId/', {recipeId: '@pk'}),
		liquidApi = $resource('/liquids/:liquidId/', {liquidId: '@pk'}),
		valveApi = $resource('/valves/:valveId/', {valveId: '@pk'});

	return {
		getRecipes: function () {
			return recipeApi.query();
		},
		getLiquids: function() {
			return liquidApi.query();
		},
		addLiquid: function(liquid, callback) {
			liquidApi.save(liquid, callback);
		},
		editLiquid: function(liquid, callback) {
			liquid.$save(callback);
		},
		getValves: function() {
			return valveApi.query();
		},
		editValve: function(valve, callback) {
			vale.$save(callback);
		},
		getRecipe: function (pk) {
			return recipeApi.get({recipeId: pk});
		},
		saveRecipe: function (recipe, callback) {
			recipe.$save(callback);
			// recipeApi.save({key: value}, function() )
		},
		deleteRecipe: function (recipe, callback) {
			recipe.$delete(callback);
		},
		newRecipe: function () {
			return new recipeApi({name: 'Untitled', components: []});
		}
	};
}]);
