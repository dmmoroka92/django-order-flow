from django.contrib import admin

from products.models import Inventory, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin[Product]):
    list_display = ("id", "name", "sku", "unit_price", "created_at")
    search_fields = ("name", "sku")  # Register your models here.


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin[Inventory]):
    list_display = ("id", "product", "quantity", "updated_at")
    search_fields = ("product__name", "product__sku")
