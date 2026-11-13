import pytest
from rest_framework.test import APIClient

from accounts.models import User
from shipments.models import Shipment


@pytest.mark.django_db
class TestShipmentListCreateView:
    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

    def test_create_shipment(self, user: User) -> None:
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/shipments/",
            {
                "reference_number": "SHIP-123",
                "status": Shipment.Status.DRAFT,
                "created_by": user.id,
            },
        )

        assert response.status_code == 201

        assert Shipment.objects.count() == 1
        assert Shipment.objects.get().created_by == user
        assert Shipment.objects.get().reference_number == "SHIP-123"
        assert Shipment.objects.get().status == Shipment.Status.DRAFT

    def test_invalid_shipment_creation(self, user: User) -> None:
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post(
            "/api/shipments/",
            {
                "reference_number": "",
                "status": Shipment.Status.DRAFT,
                "created_by": user.id,
            },
        )

        assert response.status_code == 400
        assert Shipment.objects.count() == 0
