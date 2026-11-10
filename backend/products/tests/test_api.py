from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from accounts.models import User
from products.models import Inventory, Product


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


@pytest.mark.django_db
class TestInventoryAPI:
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

    @pytest.fixture
    def inventory(self, product: Product) -> Inventory:
        return Inventory.objects.create(
            product=product,
            quantity=10,
        )

    # INDEX: GET /api/inventories/
    def test_list_inventories(self, client: APIClient, inventory: Inventory) -> None:
        response = client.get("/api/inventories/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["id"] == inventory.pk
        assert response.data[0]["quantity"] == 10

    # SHOW: GET /api/inventories/{id}/
    def test_retrieve_inventory(self, client: APIClient, inventory: Inventory) -> None:
        response = client.get(f"/api/inventories/{inventory.pk}/")

        assert response.status_code == 200
        assert response.data["id"] == inventory.pk
        assert response.data["quantity"] == 10
        assert response.data["product"]["sku"] == "LAP-001"

    # CREATE: POST /api/inventories/
    def test_create_inventory(self, client: APIClient, product: Product) -> None:
        response = client.post(
            "/api/inventories/",
            {
                "product_id": product.pk,
                "quantity": 20,
            },
            format="json",
        )

        assert response.status_code == 201
        assert Inventory.objects.filter(product=product).exists()
        assert response.data["quantity"] == 20

    # UPDATE: PATCH /api/inventories/{id}/
    def test_cannot_update_inventory(self, client: APIClient, inventory: Inventory) -> None:
        response = client.patch(
            f"/api/inventories/{inventory.pk}/",
            {"quantity": 25},
            format="json",
        )

        assert response.status_code == 405

        inventory.refresh_from_db()
        assert inventory.quantity == 10

    # DESTROY: DELETE /api/inventories/{id}/
    def test_cannot_delete_inventory(self, client: APIClient, inventory: Inventory) -> None:
        inventory_id = inventory.pk

        response = client.delete(f"/api/inventories/{inventory_id}/")

        assert response.status_code == 405
        assert Inventory.objects.filter(pk=inventory_id).exists()
