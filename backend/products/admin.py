from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin[Product]):
    list_display = ("id", "name", "sku", "unit_price", "created_at")
    search_fields = ("name", "sku")  # Register your models here.
