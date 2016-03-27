

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

.controller('MainCtrl', ['$scope', 'RestApi', function ($scope, RestApi) {
	$scope.recipes = RestApi.getRecipes()
	$scope.view = {value: 'home'};
}])

.factory('RestApi', ['$resource', function ($resource) {
	var recipeApi = $resource('/recipes/:recipeId', {recipeId: 'recipe_pk'});

	return {
		getRecipes: function () {
			return recipeApi.query();
		}
	};
}]);
