from django.contrib import admin
from .models import Price, Store, Product

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'price')

    def store_name(self, obj):
        return obj.store.name

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)