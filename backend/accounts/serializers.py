from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class ManagerCreateSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name"]
        read_only_fields = ["id"]

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        data = super().validate(attrs)

        user = self.user

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "firstName": user.first_name,
            "lastName": user.last_name,
        }

        return data
