import pytest
from django.urls import reverse
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


@pytest.mark.django_db
class TestManagerCreation:
    def test_superadmin_can_create_manager(self) -> None:
        superadmin = User.objects.create_superuser(
            email="admin@example.com",
            password="Admin@2026#Secure!",
        )

        client = APIClient()
        client.force_authenticate(user=superadmin)

        response = client.post(
            reverse("manager-create"),
            {
                "email": "manager@example.com",
                "password": "Manager@2026#Secure!",
                "first_name": "John",
                "last_name": "Smith",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        manager = User.objects.get(email="manager@example.com")

        assert manager.is_superuser is False
        assert manager.is_staff is False
        assert manager.check_password("Manager@2026#Secure!")
        assert "password" not in response.data

    def test_regular_user_cannot_create_manager(self) -> None:
        manager = User.objects.create_user(
            email="manager@example.com",
            password="Manager@2026#Secure!",
        )

        client = APIClient()
        client.force_authenticate(user=manager)

        response = client.post(
            reverse("manager-create"),
            {
                "email": "another-manager@example.com",
                "password": "Manager@2026#Secure!",
                "first_name": "Jane",
                "last_name": "Smith",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not User.objects.filter(email="another-manager@example.com").exists()

    def test_unauthenticated_user_cannot_create_manager(self) -> None:
        client = APIClient()

        response = client.post(
            reverse("manager-create"),
            {
                "email": "manager@example.com",
                "password": "Manager@2026#Secure!",
                "first_name": "John",
                "last_name": "Smith",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not User.objects.filter(email="manager@example.com").exists()

    def test_cannot_create_manager_with_duplicate_email(self) -> None:
        superadmin = User.objects.create_superuser(
            email="admin@example.com",
            password="Admin@2026#Secure!",
        )

        User.objects.create_user(
            email="manager@example.com",
            password="Manager@2026#Secure!",
        )

        client = APIClient()
        client.force_authenticate(user=superadmin)

        response = client.post(
            reverse("manager-create"),
            {
                "email": "manager@example.com",
                "password": "AnotherManager@2026!",
                "first_name": "Jane",
                "last_name": "Smith",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert User.objects.filter(email="manager@example.com").count() == 1

    def test_cannot_create_manager_with_weak_password(self) -> None:
        superadmin = User.objects.create_superuser(
            email="admin@example.com",
            password="Admin@2026#Secure!",
        )

        client = APIClient()
        client.force_authenticate(user=superadmin)

        response = client.post(
            reverse("manager-create"),
            {
                "email": "manager@example.com",
                "password": "123",
                "first_name": "John",
                "last_name": "Smith",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data
        assert not User.objects.filter(email="manager@example.com").exists()
