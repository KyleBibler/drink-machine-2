from django.contrib import admin
from .models import Valve, Liquid, Recipe, LiquidAmount, DrinkRequest

def make_open_135(modeladmin, request, queryset):
	queryset.update(angle_open=45, angle_closed=135)
	make_open_135.short_description = "Make angle open 135 and angle closed 45"

class ValveAdmin(admin.ModelAdmin):
	ordering = ['servo_pin']
	actions = [make_open_135]


admin.site.register(Valve, ValveAdmin)
admin.site.register(Liquid)
admin.site.register(Recipe)
admin.site.register(LiquidAmount)
admin.site.register(DrinkRequest)
