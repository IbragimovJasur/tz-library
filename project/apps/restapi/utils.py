from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken


BaseUser = get_user_model()  # BaseUser model

def get_access_refresh_token_for_user(user: BaseUser) -> dict:
    """Generating access and refresh tokens for BaseUser model"""

    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
