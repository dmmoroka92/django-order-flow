from django.db import transaction

from products.models import Inventory


class InsufficientStockError(Exception):
    pass


class StockService:
    @staticmethod
    @transaction.atomic
    def restock(inventory_id: int, quantity: int) -> None:
        if type(quantity) is not int:
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        inventory = Inventory.objects.select_for_update().get(pk=inventory_id)

        inventory.quantity += quantity
        inventory.save(update_fields=["quantity", "updated_at"])

    @staticmethod
    @transaction.atomic
    def remove_stock(inventory_id: int, quantity: int) -> None:
        if type(quantity) is not int:
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        inventory = Inventory.objects.select_for_update().get(pk=inventory_id)

        if inventory.quantity < quantity:
            raise InsufficientStockError(
                f"Insufficient stock. Available: {inventory.quantity}, Requested: {quantity}"
            )

        inventory.quantity -= quantity
        inventory.save(update_fields=["quantity", "updated_at"])
