from django.apps import apps
from drink_maker.models import Recipe, Valve, DrinkRequest, Liquid, LiquidAmount
from drink_maker.managers import ScaleManager, ServoManager
import time

def add_request(recipe_name):
	try:
		recipe = Recipe.objects.get(name=recipe_name)
	except Recipe.DoesNotExist:
		recipe = None
	if recipe is None:
		return False
	req = DrinkRequest(recipe=recipe)
	req.save()
	return make_drink(recipe)

def make_drink(recipe):
	print "Making that drink"
