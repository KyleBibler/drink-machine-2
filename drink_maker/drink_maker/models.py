from django.db import models

class Valve(models.Model):
	is_registered = models.BooleanField(default=False)
	servo_pin = models.IntegerField(unique=True)
	angle_closed = models.IntegerField()
	angle_open = models.IntegerField()

	def __repr__(self):
		return "<Valve - Pin: %s>" % str(self.servo_pin)

	def __unicode__(self):
		return "Valve - Pin: %s" % str(self.servo_pin)

class Liquid(models.Model):
	name = models.CharField(max_length=128)
	is_available = models.BooleanField(default=False)
	density = models.DecimalField(default=1.0, max_digits=6, decimal_places=4)
	valve = models.OneToOneField(Valve, blank=True, null=True)

	def __repr__(self):
		return "<Liquid: %s>" % str(self.name)

	def __unicode__(self):
		return "Liquid: %s" % str(self.name)

class Recipe(models.Model):
	name = models.CharField(max_length=128)
	components = models.ManyToManyField(Liquid, through='LiquidAmount')

	def __repr__(self):
		return "<Recipe: %s>" % str(self.name)

	def __unicode__(self):
		return "Recipe: " + str(self.name) + " - \n" + ", ".join([c.name for c in self.components.all()])

class LiquidAmount(models.Model):
	recipe = models.ForeignKey(Recipe)
	liquid = models.ForeignKey(Liquid)
	#volume in mL
	volume = models.DecimalField(max_digits=8, decimal_places=1) 

	def __repr__(self):
		return "<Recipe: %s - Liquid: %s %smL>" % (str(self.recipe.name), str(self.liquid.name), str(self.volume))

	def __unicode__(self):
		return "Recipe: %s - Liquid: %s %smL" % (str(self.recipe.name), str(self.liquid.name), str(self.volume))

class DrinkRequest(models.Model):
	recipe = models.ForeignKey(Recipe)
	time_stamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "Request: %s - %s" % (str(self.recipe.name), str(self.time_stamp))