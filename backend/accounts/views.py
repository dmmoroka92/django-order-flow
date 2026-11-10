from typing import Any, cast

from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.permissions import IsSuperadmin
from accounts.serializers import ManagerCreateSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def _belongs_to_user(self, token: RefreshToken, user: User) -> bool:
        token_user_id = token.payload.get(api_settings.USER_ID_CLAIM)

        return token_user_id is not None and str(token_user_id) == str(user.pk)

    def post(self, request: Request) -> Response:
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
            token = RefreshToken(cast(Any, refresh_token))
            user = request.user

            if not isinstance(user, User) or not self._belongs_to_user(token, user):
                return Response(
                    {"detail": "Invalid refresh token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token.blacklist()

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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


class ManagerCreateView(generics.CreateAPIView[User]):
    serializer_class = ManagerCreateSerializer
    permission_classes = [IsAuthenticated, IsSuperadmin]
