from decimal import Decimal

import pytest

from products.models import Inventory, Product
from products.services.stock_service import (
    InsufficientStockError,
    StockService,
)


@pytest.mark.django_db
class TestStockService:
    @pytest.fixture
    def inventory(self) -> Inventory:
        product = Product.objects.create(
            name="Test Product",
            sku="TEST-123",
            unit_price=Decimal("10.00"),
        )

        return Inventory.objects.create(
            product=product,
            quantity=10,
        )

    # RESTOCK

    def test_restock_increases_quantity(self, inventory: Inventory) -> None:
        StockService.restock(inventory.id, 5)

        inventory.refresh_from_db()

        assert inventory.quantity == 15

    def test_restock_rejects_zero_quantity(self, inventory: Inventory) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero",
        ):
            StockService.restock(inventory.id, 0)

    def test_restock_rejects_negative_quantity(self, inventory: Inventory) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero",
        ):
            StockService.restock(inventory.id, -5)

    def test_restock_rejects_non_integer_quantity(self, inventory: Inventory) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be an integer",
        ):
            StockService.restock(inventory.id, 5.5)  # type: ignore[arg-type]

    def test_restock_inventory_not_found(self) -> None:
        with pytest.raises(Inventory.DoesNotExist):
            StockService.restock(999999, 5)

    # REMOVE STOCK

    def test_remove_stock_decreases_quantity(self, inventory: Inventory) -> None:
        StockService.remove_stock(inventory.id, 5)

        inventory.refresh_from_db()

        assert inventory.quantity == 5

    def test_remove_stock_rejects_zero_quantity(self, inventory: Inventory) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero",
        ):
            StockService.remove_stock(inventory.id, 0)

    def test_remove_stock_rejects_negative_quantity(self, inventory: Inventory) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero",
        ):
            StockService.remove_stock(inventory.id, -5)

    def test_remove_stock_rejects_insufficient_stock(self, inventory: Inventory) -> None:
        with pytest.raises(InsufficientStockError):
            StockService.remove_stock(inventory.id, 15)

        inventory.refresh_from_db()

        assert inventory.quantity == 10

    def test_remove_stock_inventory_not_found(self) -> None:
        with pytest.raises(Inventory.DoesNotExist):
            StockService.remove_stock(999999, 5)
