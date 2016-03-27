from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext

from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .managers import ServoManager, ScaleManager, DrinkManager
from .models import Recipe, Liquid, Valve, LiquidAmount, DrinkRequest
import os, json

from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse

def index(request):
	print "I am here"
	return render(request, 'drink_maker/index.html')

def valves(request):
	if request.method == 'POST':
		#Register a liquid to a valve
		errors = []
		if(all(x in request.POST for x in ['gpin', 'angle_closed', 'angle_open'])):
			if('valve_pk' in request.POST):
				#Update a valve
				try:
					valve = Valve.objects.get(pk=request.POST["valve_pk"])
				except Valve.DoesNotExist:
					valve = None
					errors.append("Valve does not exist")
					success = False
			else:
				#Make a new valve
				valve = Valve()
			if valve is not None:
				valve.servo_pin = request.POST["gpin"]
				valve.angle_closed = request.POST["angle_closed"]
				valve.angle_open = request.POST["angle_open"]				
				valve.save()
				success = True
		else:
			success = False
			errors.append("Not all necessary fields (gpin, angle_open, angle_closed) were provied")
		data = {"success": success, "errors": errors}
	elif request.method == 'GET':
		#Get list of all current liquid registrations
		print "Getting all valve registrations"
		data = serialize_valves(Valve.objects.all())
	return HttpResponse(json.dumps(data), content_type="application/json")

def liquids(request):
	if request.method == 'POST':
		#Register, update, or delete a liquid
		errors = []
		liquid = None
		print request.POST
		if('liquid_pk' in request.POST):
			#Update this liquid			
			try:
				liquid = Liquid.objects.get(pk=request.POST["liquid_pk"])
			except Liquid.DoesNotExist:
				success = False
				errors.append("Liquid does not exist")
		elif 'name' in request.POST:
			liquid = Liquid()
		else:
			success = False
			errors.append("Not all necessary fields () were provied")
		if liquid is not None:
			if 'name' in request.POST:
				liquid.name = request.POST['name']
			if 'density' in request.POST:
				liquid.density = request.POST['density']
			if 'valve_pk' in request.POST:
				try:
					valve = Valve.objects.get(pk=request.POST["valve_pk"])
					liquid.valve = valve
				except Valve.DoesNotExist:
					valve = None
					errors.append("Valve does not exist; liquid will still be created")
			liquid.save()
			success = True			
		data = {"success": success, "errors": errors}
	elif request.method == 'GET':
		#Get all liquids or a single liquid
		if "name" in request.GET:
			#get the specific recipe
			try:
				liquid = Liquid.objects.get(name=request.GET["name"])
			except Liquid.DoesNotExist:
				liquid = {}
			data = serialize_liquids([liquid])
		else:
			data = serialize_liquids(Liquid.objects.all())
	return HttpResponse(json.dumps(data), content_type="application/json")
			
def recipes(request):
	if request.method == 'POST':
		#Register a new recipe
		errors = []		
		if('recipe_pk' in request.POST):
			#Update this recipe
			try:
				recipe = Recipe.objects.get(pk=request.POST["recipe_pk"])
			except Recipe.DoesNotExist:
				recipe = None
				success = False
				errors.append("Recipe does not exist")
		elif(any(x in request.POST for x in ['name', 'components'])):
			recipe = Recipe()		
		if recipe is not None:
			if 'delete' in request.POST and request.POST['delete'] is True:					
				#delete this recipe
				recipe.delete()
				success = true
			else:
				if 'name' in request.POST:
					recipe.name = request.POST['name']
				if 'components' in request.POST:
					for component in request.POST['components']:
						try:
							liquid = Liquid.objects.get(pk=component.pk)
							c_field = LiquidAmount(recipe=recipe, liquid=liquid, volume=component.volume)
						except Liquid.DoesNotExist:
							liquid = None
							errors.append("Liquid did not exist, please add it before making a recipe")	
				recipe.save()
				success = True
		else:
			success = False
			errors.append("Not all necessary fields were provied or recipe does not exist.")
		data = {"success": success, "errors": errors}
	elif request.method == 'GET':
		#Get all recipes or a specific recipe
		if "name" in request.GET:
			#get the specific recipe
			try:
				recipe = Recipe.objects.get(name=request.GET["name"])
			except Recipe.DoesNotExist:
				recipe = {}
			data = serialize_recipes([recipe])
		else:
			data = serialize_recipes(Recipe.objects.all())
	return HttpResponse(json.dumps(data), content_type="application/json")


def drinks(request):
	print "\n=============================\nDRANK\n=============================\n"
	if request.method == 'POST':
		#Make a drink?
		errors = []
		if 'recipe_name' not in request.POST:
			success = False
		if DrinkRequest.objects.all().count() > 0:
			success = False
		else:
			DrinkManager.add_request(request.POST['recipe_name'])
		data = json.dumps({"success": success})
	elif request.method == 'GET':
		data = serializers.serialize('json', DrinkRequest.objects.all())
	return HttpResponse(json.dumps(data), content_type="application/json")

def serialize_recipes(recipes):
	result = []
	for recipe in recipes:
		r = {}
		r["pk"] = recipe.pk
		r["name"] = recipe.name
		recipe_components = []
		for comp in recipe.liquidamount_set.all():
			c = {}
			c["name"] = comp.liquid.name
			c["volume"] = str(comp.volume)
			recipe_components.append(c)
		r["components"] = recipe_components
		result.append(r)
	return result

def serialize_valves(valves):
	result = []
	for valve in valves:
		v = {}
		v["pk"] = valve.pk
		v["servo_pin"] = valve.servo_pin
		v["liquid"] = valve.liquid.name	
		result.append(v)
	return result

def serialize_liquids(liquids):
	result = []
	for liquid in liquids:
		l = {}
		l["pk"] = liquid.pk
		l["name"] = liquid.name
		if liquid.valve is not None:
			l["valve"] = liquid.valve.pk
			l["valve_pin"] = liquid.valve.servo_pin
		else:
			l["valve"] = None
		result.append(l)
	return result