from django.contrib import admin
from .models import Valve, Liquid, Recipe, LiquidAmount, DrinkRequest


admin.site.register(Valve)
admin.site.register(Liquid)
admin.site.register(Recipe)
admin.site.register(LiquidAmount)
admin.site.register(DrinkRequest)