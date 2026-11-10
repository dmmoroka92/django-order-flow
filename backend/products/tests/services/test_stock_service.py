from decimal import Decimal

import pytest

from products.models import Inventory, Product
from products.services.exceptions import InsufficientStockError
from products.services.stock_service import StockService


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

    @pytest.mark.parametrize("quantity", [0, -5])
    def test_restock_rejects_invalid_quantity(self, inventory: Inventory, quantity: int) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero",
        ):
            StockService.restock(inventory.id, quantity)

        inventory.refresh_from_db()
        assert inventory.quantity == 10

    @pytest.mark.parametrize("quantity", [5.5, "5", True])
    def test_restock_rejects_non_integer_quantity(
        self, inventory: Inventory, quantity: object
    ) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be an integer",
        ):
            StockService.restock(
                inventory.id,
                quantity,  # type: ignore[arg-type]
            )

        inventory.refresh_from_db()
        assert inventory.quantity == 10

    def test_restock_inventory_not_found(self) -> None:
        with pytest.raises(Inventory.DoesNotExist):
            StockService.restock(999999, 5)

    # REMOVE STOCK

    def test_remove_stock_decreases_quantity(self, inventory: Inventory) -> None:
        StockService.remove_stock(inventory.id, 5)

        inventory.refresh_from_db()

        assert inventory.quantity == 5

    def test_remove_all_available_stock(self, inventory: Inventory) -> None:
        StockService.remove_stock(inventory.id, 10)

        inventory.refresh_from_db()

        assert inventory.quantity == 0

    @pytest.mark.parametrize("quantity", [0, -5])
    def test_remove_stock_rejects_invalid_quantity(
        self, inventory: Inventory, quantity: int
    ) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero",
        ):
            StockService.remove_stock(inventory.id, quantity)

        inventory.refresh_from_db()
        assert inventory.quantity == 10

    @pytest.mark.parametrize("quantity", [5.5, "5", True])
    def test_remove_stock_rejects_non_integer_quantity(
        self, inventory: Inventory, quantity: object
    ) -> None:
        with pytest.raises(
            ValueError,
            match="Quantity must be an integer",
        ):
            StockService.remove_stock(
                inventory.id,
                quantity,  # type: ignore[arg-type]
            )

        inventory.refresh_from_db()
        assert inventory.quantity == 10

    def test_remove_stock_rejects_insufficient_stock(self, inventory: Inventory) -> None:
        with pytest.raises(
            InsufficientStockError,
            match="Insufficient stock",
        ):
            StockService.remove_stock(inventory.id, 15)

        inventory.refresh_from_db()

        assert inventory.quantity == 10

    def test_remove_stock_inventory_not_found(self) -> None:
        with pytest.raises(Inventory.DoesNotExist):
            StockService.remove_stock(999999, 5)
