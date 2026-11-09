# Create your tests here.
import pytest

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
