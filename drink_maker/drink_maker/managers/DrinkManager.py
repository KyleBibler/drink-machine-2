from django.apps import apps
from drink_maker.models import Recipe, Valve, DrinkRequest, Liquid, LiquidAmount
from drink_maker.managers import ScaleManager, ServoManager
import time

def add_request(recipe_pk):
	try:
		recipe = Recipe.objects.get(pk=recipe_pk)
	except Recipe.DoesNotExist:
		recipe = None
	if recipe is None:
		return False
	print "Making recipe " + str(recipe.name)
	req = DrinkRequest(recipe=recipe)
	req.save()
	make_drink(recipe)
	req.delete()

def make_drink(recipe):
	print "Making that drink"
	for comp in recipe.liquidamount_set.all():
		valve = comp.liquid.valve
		target_weight = comp.volume * comp.liquid.density
		print "Putting in " + str(target_weight) + " grams of " + str(comp.liquid.name)
		if ScaleManager.device_ready():
			tare = ScaleManager.get_data()
			print "The tare is " + str(tare)
			if tare > 0:
				#target_weight += tare
				accumulation = 0
				print "The target weight is " + str(target_weight)
				#there is a cup on the scale
				pwm = ServoManager.set_pin(valve.servo_pin)
				ServoManager.set_angle(pwm, valve.angle_open)
				ServoManager.tear_down(pwm,valve.servo_pin)
				cutoff_time = time.time() + 10
				current_scale_data = ScaleManager.get_data()
				prev_scale_data = current_scale_data
				while accumulation < target_weight and time.time() < cutoff_time:
					current_scale_data = ScaleManager.get_data()
					if current_scale_data != prev_scale_data:
						accumulation += current_scale_data
						prev_scale_data = current_scale_data
					time.sleep(0.01)
				print "Scale Data " + str(ScaleManager.get_data())
				ServoManager.set_pin(valve.servo_pin, old_pwm=pwm)
				ServoManager.set_angle(pwm,valve.angle_closed)
				ServoManager.tear_down(pwm,valve.servo_pin)
		else:
			print "SCALE MANAGER IS NOT READY?"
	#time.sleep(3)
	return True


	
