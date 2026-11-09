from typing import Any, cast

from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        # DRF can parse JSON objects or arrays.
        # Our endpoint requires a JSON object.
        if not isinstance(request.data, dict):
            return Response(
                {"detail": "Expected a JSON object."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh_token = request.data.get("refresh")

        if not isinstance(refresh_token, str) or not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Simple JWT accepts a token string at runtime.
            # The cast works around an incorrect/incomplete stub.
            token = RefreshToken(cast(Any, refresh_token))
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Confirm the refresh token belongs to the authenticated user.
        # This check should be performed BEFORE blacklisting.
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user

        if not isinstance(user, User):
            raise NotAuthenticated()

        return Response(
            {
                "id": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        )
