
var recipes = [],
	liquids = [],
	valves = [],
	views = ["drink-maker-container","recipe-editor-container","liquid-editor-container","valve-config-container"];

var loadDrinkMakerHtml = function(recipes) {
	var html = '<div class="row">';
	recipes.forEach(function(recipe) {
		html += '<div class="col-lg-6 col-md-6 col-sm-12">';
		html += '<div class="panel panel-primary dm-recipe-container">'
		html += '<div class="panel-heading"><h2 class="panel-title">' + recipe.name + '</h2></div>';
		html += '<div class="panel-body">';
		recipe.components.forEach(function(c) {
			html += '<p><span class="bold">' + c.name + ':</span> ' + c.volume + 'mL</p>';
		});
		html += '</div></div></div>';
	});
	html += '</div>';
	$("#dmRecipesContainer").html(html);
};

var swapViews = function(view) {
	views.forEach(function(v) {
		if(view !== v) { $('.'+v).hide(); }
	});
	$('.'+view).show();
}

var loadRecipeHtml = function(recipes) {
	var html = "";
	recipes.forEach(function(recipe) {
		html += '<div class="re-recipe-container>"';

		html += '</div>';
	});
}

var getRecipes = function() {
	$.ajax({
		url: "/recipes/",
	    type: "GET",
	    success: function(json) {
	      	recipes = json["recipes"];

	    	loadDrinkMakerHtml(recipes);
	    	loadRecipeHtml(recipes);
	    }
	});
};

var getValves = function() {
	$.ajax({
		url: "/valves/",
	    type: "GET",
	    success: function(json) {
	      	valves = json["valves"];
	    }
	});
};

var getLiquids = function() {
	$.ajax({
		url: "/liquids/",
	    type: "GET",
	    success: function(json) {
	      	liquids = json["liquids"];
	    }
	});
};

var pollDrinkRequest = function() {
	$.ajax({
		url: "/drinks/",
	    type: "GET",
	    success: function(json) {
	      	if(json.length > 0) {
	      		console.log("There is a request being fulfilled");
	      	}
	    }
	});
}

getRecipes();