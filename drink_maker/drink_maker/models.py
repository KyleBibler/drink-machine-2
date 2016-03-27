from django.db import models

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Valve(models.Model):
	servo_pin = models.IntegerField(unique=True)
	angle_closed = models.IntegerField()
	angle_open = models.IntegerField()

	def __repr__(self):
		return "<Valve - Pin: %s>" % str(self.servo_pin)

	def __unicode__(self):
		return "Valve - Pin: %s" % str(self.servo_pin)

class Liquid(models.Model):
	name = models.CharField(max_length=128)
	density = models.DecimalField(default=1.0, max_digits=6, decimal_places=2)
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
	volume = IntegerRangeField(min_value=1, max_value=450, default=45) 

	def __repr__(self):
		return "<Recipe: %s - Liquid: %s %smL>" % (str(self.recipe.name), str(self.liquid.name), str(self.volume))

	def __unicode__(self):
		return "Recipe: %s - Liquid: %s %smL" % (str(self.recipe.name), str(self.liquid.name), str(self.volume))

class DrinkRequest(models.Model):
	recipe = models.ForeignKey(Recipe)
	time_stamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "Request: %s - %s" % (str(self.recipe.name), str(self.time_stamp))