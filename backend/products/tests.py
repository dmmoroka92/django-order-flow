from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from accounts.models import User
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


@pytest.mark.django_db
class TestProductAPI:
    @pytest.fixture
    def client(self) -> APIClient:
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="StrongPassword123!",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @pytest.fixture
    def product(self) -> Product:
        return Product.objects.create(
            name="MacBook Pro",
            sku="LAP-001",
            unit_price=Decimal("1999.99"),
        )

    # INDEX: GET /api/products/
    def test_list_products(self, client: APIClient, product: Product) -> None:
        response = client.get("/api/products/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == product.pk
        assert response.data[0]["name"] == "MacBook Pro"

    # SHOW: GET /api/products/{id}/
    def test_retrieve_product(self, client: APIClient, product: Product) -> None:
        response = client.get(f"/api/products/{product.pk}/")

        assert response.status_code == 200
        assert response.data["id"] == product.pk
        assert response.data["sku"] == "LAP-001"

    # CREATE: POST /api/products/
    def test_create_product(self, client: APIClient) -> None:
        response = client.post(
            "/api/products/",
            {
                "name": "iPhone 16",
                "sku": "PHN-001",
                "unit_price": "799.99",
            },
            format="json",
        )

        assert response.status_code == 201
        assert Product.objects.filter(sku="PHN-001").exists()
        assert response.data["name"] == "iPhone 16"

    # UPDATE: PATCH /api/products/{id}/
    def test_update_product(self, client: APIClient, product: Product) -> None:
        response = client.patch(
            f"/api/products/{product.pk}/",
            {"unit_price": "1799.99"},
            format="json",
        )

        assert response.status_code == 200

        product.refresh_from_db()
        assert product.unit_price == Decimal("1799.99")

    # DESTROY: DELETE /api/products/{id}/
    def test_delete_product(self, client: APIClient, product: Product) -> None:
        response = client.delete(f"/api/products/{product.pk}/")

        assert response.status_code == 204
        assert not Product.objects.filter(pk=product.pk).exists()
