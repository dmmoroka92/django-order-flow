# Create your tests here.
import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db
def test_create_user() -> None:
    user = User.objects.create_user(
        email="manager@example.com",
        password="test-password-123",
        first_name="John",
        last_name="Smith",
    )

    assert user.email == "manager@example.com"
    assert user.is_superuser is False
    assert user.is_staff is False
    assert user.check_password("test-password-123")


@pytest.mark.django_db
def test_login_returns_tokens() -> None:
    User.objects.create_user(
        email="manager@example.com",
        password="test-password-123",
        first_name="John",
        last_name="Smith",
    )

    client = APIClient()

    response = client.post(
        "/api/auth/login/", {"email": "manager@example.com", "password": "test-password-123"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
class TestMeEndpoint:
    @pytest.fixture
    def user(self) -> User:
        return User.objects.create_user(
            email="manager@example.com",
            password="secure-password-123",
        )

    @pytest.fixture
    def response(self, user: User) -> Response:
        client = APIClient()

        client.force_authenticate(user=user)

        return client.get("/api/auth/me/")

    def test_returns_200_ok(self, response: Response) -> None:
        assert response.status_code == status.HTTP_200_OK

    def test_returns_authenticated_user_id(self, response: Response, user: User) -> None:
        assert response.data["id"] == user.pk

    def test_returns_authenticated_user_email(self, response: Response, user: User) -> None:
        assert response.data["email"] == user.email

    def test_does_not_expose_password(self, response: Response) -> None:
        assert "password" not in response.data
