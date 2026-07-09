from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class TokenRefreshView(APIView):
    """Exchange a valid refresh token for a new access token.

    Accepts {"refresh_token": ...} (matches the login response shape) and
    returns {"access_token": ...}.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("refresh_token") or request.data.get("refresh")
        if not token:
            return Response(
                {"error": "refresh_token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(token)
        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token", "code": "token_not_valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            {"access_token": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
