from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from products.models import Product


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
