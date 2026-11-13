from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from accounts.models import User
from products.models import Product
from shipments.models import Shipment, ShipmentItem


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def shipment(user: User) -> Shipment:
    return Shipment.objects.create(
        reference_number="SHIP-123",
        status=Shipment.Status.DRAFT,
        created_by=user,
    )


@pytest.mark.django_db
class TestShipment:
    def test_valid_shipment_creation(self, shipment: Shipment, user: User) -> None:
        assert shipment.pk is not None
        assert shipment.reference_number == "SHIP-123"
        assert shipment.status == Shipment.Status.DRAFT
        assert shipment.created_by == user
        assert shipment.created_at is not None
        assert shipment.updated_at is not None

    @pytest.mark.parametrize("reference_number", [""])
    def test_invalid_reference_number(self, user: User, reference_number: str) -> None:
        shipment = Shipment(
            reference_number=reference_number,
            status=Shipment.Status.DRAFT,
            created_by=user,
        )
        with pytest.raises(ValidationError):
            shipment.full_clean()

    def test_shipment_total_value(self, shipment: Shipment) -> None:
        product1 = Product.objects.create(
            name="Test Product",
            sku="TEST-123",
            unit_price=Decimal("100.00"),
        )

        product2 = Product.objects.create(
            name="Test Product 2",
            sku="TEST-456",
            unit_price=Decimal("150.00"),
        )

        ShipmentItem.objects.create(
            shipment=shipment,
            product=product1,
            quantity=2,
            unit_price=product1.unit_price,
        )

        ShipmentItem.objects.create(
            shipment=shipment,
            product=product2,
            quantity=2,
            unit_price=product2.unit_price,
        )

        assert shipment.total_value() == Decimal("500.00")

    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (Shipment.Status.DRAFT, True),
            (Shipment.Status.CONFIRMED, False),
            (Shipment.Status.SHIPPED, False),
            (Shipment.Status.DELIVERED, False),
            (Shipment.Status.CANCELLED, False),
        ],
    )
    def test_shipment_is_editable(
        self, shipment: Shipment, status: Shipment.Status, expected: bool
    ) -> None:
        shipment.status = status

        assert shipment.is_editable() is expected

    def test_shipment_str(self, shipment: Shipment) -> None:
        assert str(shipment) == "Shipment SHIP-123 (draft)"


@pytest.mark.django_db
class TestShipmentItem:
    @pytest.fixture
    def product(self) -> Product:
        return Product.objects.create(
            name="Test Product",
            sku="TEST-123",
            unit_price=Decimal("100.00"),
        )

    @pytest.fixture
    def shipment_item(self, shipment: Shipment, product: Product) -> ShipmentItem:
        return ShipmentItem.objects.create(
            shipment=shipment,
            product=product,
            quantity=2,
            unit_price=product.unit_price,
        )

    def test_valid_shipment_item_creation(self, shipment: Shipment, product: Product) -> None:
        shipment_item = ShipmentItem.objects.create(
            shipment=shipment,
            product=product,
            quantity=2,
            unit_price=product.unit_price,
        )

        assert shipment_item.pk is not None
        assert shipment_item.shipment == shipment
        assert shipment_item.product == product
        assert shipment_item.quantity == 2
        assert shipment_item.unit_price == product.unit_price

    def test_invalid_shipment_item_creation(
        self,
        shipment: Shipment,
        product: Product,
    ) -> None:
        shipment_item = ShipmentItem(
            shipment=shipment,
            product=product,
            quantity=-1000,
            unit_price=product.unit_price,
        )

        with pytest.raises(ValidationError) as exc:
            shipment_item.full_clean()

        assert ShipmentItem.objects.count() == 0
        assert "quantity" in exc.value.message_dict

    def test_shipment_item_str(self, shipment_item: ShipmentItem) -> None:
        assert str(shipment_item) == "SHIP-123 - TEST-123 x 2"
