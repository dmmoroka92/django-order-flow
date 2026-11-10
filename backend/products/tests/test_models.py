from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from products.models import Inventory, Product


@pytest.mark.django_db
class TestValidProductCreation:
    def test_create_product(self) -> None:
        product = Product.objects.create(
            name="Test Product",
            sku="TEST-123",
            unit_price=10.00,
        )

        assert product.pk is not None
        assert product.name == "Test Product"
        assert product.sku == "TEST-123"
        assert product.unit_price == 10.00
        assert product.created_at is not None
        assert product.updated_at is not None


@pytest.mark.django_db
class TestProductValidation:
    def test_name_is_required(self) -> None:
        product = Product(
            name="",
            sku="TEST-123",
            unit_price=10.00,
        )

        with pytest.raises(ValidationError) as exc:
            product.full_clean()

        assert "Product name is required." in exc.value.message_dict["name"]

    def test_name_max_length_is_255(self) -> None:
        product = Product(
            name="A" * 256,
            sku="TEST-123",
            unit_price=10.00,
        )

        with pytest.raises(ValidationError) as exc:
            product.full_clean()

        assert "Product name must not exceed 255 characters." in exc.value.message_dict["name"]

    def test_sku_is_required(self) -> None:
        product = Product(
            name="Test Product",
            sku="",
            unit_price=10.00,
        )

        with pytest.raises(ValidationError) as exc:
            product.full_clean()

        assert "SKU is required." in exc.value.message_dict["sku"]

    def test_sku_must_be_unique(self) -> None:
        Product.objects.create(
            name="Test Product",
            sku="TEST-123",
            unit_price=Decimal("10.00"),
        )

        duplicate_product = Product(
            name="Test Product 2",
            sku="TEST-123",
            unit_price=Decimal("10.00"),
        )

        with pytest.raises(ValidationError) as exc:
            duplicate_product.full_clean()

        assert "A product with this SKU already exists." in exc.value.message_dict["sku"]

    @pytest.mark.parametrize(
        "price",
        [Decimal(0.00), Decimal(-10.00)],
    )
    def test_unit_price_must_be_positive(self, price: Decimal) -> None:
        product = Product(
            name="Test Product",
            sku="TEST-123",
            unit_price=price,
        )

        with pytest.raises(ValidationError) as exc:
            product.full_clean()

        assert "Unit price must be greater than zero." in exc.value.message_dict["unit_price"]

    def test_unit_price_is_required(self) -> None:
        product = Product(  # type: ignore[misc]
            name="Test Product",
            sku="TEST-123",
            unit_price=None,
        )

        with pytest.raises(ValidationError) as exc:
            product.full_clean()

        assert "Unit price is required." in exc.value.message_dict["unit_price"]

    def test_unit_price_must_be_decimal(self) -> None:
        product = Product(
            name="Test Product",
            sku="TEST-123",
            unit_price="invalid",
        )

        with pytest.raises(ValidationError) as exc:
            product.full_clean()

        assert "Enter a valid unit price." in exc.value.message_dict["unit_price"]


@pytest.mark.django_db
class TestInventory:
    @pytest.fixture
    def product(self) -> Product:
        return Product.objects.create(
            name="MacBook Pro",
            sku="LAP-001",
            unit_price=Decimal("1999.99"),
        )

    def test_create_inventory(self, product: Product) -> None:
        inventory = Inventory.objects.create(
            product=product,
            quantity=10,
        )

        assert inventory.pk is not None
        assert inventory.product == product
        assert inventory.quantity == 10
        assert inventory.updated_at is not None

    def test_default_quantity(self, product: Product) -> None:
        inventory = Inventory.objects.create(product=product)

        assert inventory.quantity == 0

    def test_quantity_cannot_be_negative(self, product: Product) -> None:
        inventory = Inventory(
            product=product,
            quantity=-5,
        )

        with pytest.raises(ValidationError):
            inventory.full_clean()

    def test_product_has_only_one_inventory(self, product: Product) -> None:
        Inventory.objects.create(product=product, quantity=10)

        duplicate = Inventory(product=product, quantity=20)

        with pytest.raises(ValidationError):
            duplicate.full_clean()

    def test_reverse_relationship(self, product: Product) -> None:
        inventory = Inventory.objects.create(
            product=product,
            quantity=10,
        )

        assert product.inventory == inventory

    def test_delete_product_deletes_inventory(self, product: Product) -> None:
        inventory = Inventory.objects.create(
            product=product,
            quantity=10,
        )

        inventory_id = inventory.pk
        product.delete()

        assert not Inventory.objects.filter(pk=inventory_id).exists()

    def test_string_representation(self, product: Product) -> None:
        inventory = Inventory.objects.create(
            product=product,
            quantity=10,
        )

        assert str(inventory) == "LAP-001: (10)"
