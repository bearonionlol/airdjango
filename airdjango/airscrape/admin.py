from django.contrib import admin
from .models import Price

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('stores_and_prices', 'cheapest_price')

    pass