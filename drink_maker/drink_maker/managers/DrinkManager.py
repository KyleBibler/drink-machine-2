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
	for comp in recipe.liquidamount_set.all():
		valve = comp.liquid.valve
		target_weight = comp.volume * comp.liquid.density
		if ScaleManager.device_ready():
			tare = ScaleManager.get_data()
			if tare > 0:
				target_weight += tare
				#there is a cup on the scale
				ServoManager.set_pin(valve.servo_pin)
				ServoManager.set_angle(valve.angle_open)
				ServoManager.set_pin(0)
				cutoff_time = time.time() + 10
				while ScaleManager.get_data() < target_weight and time.time() < cutoff_time:
					time.sleep(0.01)
				ServoManager.set_pin(valve.servo_pin)
				ServoManager.set_angle(valve.angle_closed)
				ServoManager.set_pin(0)
	return True


	
