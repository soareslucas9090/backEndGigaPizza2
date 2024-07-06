from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@extend_schema(tags=["Auth"])
class TokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=["Auth"])
class TokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=["Auth"])
class TokenVerifyView(TokenVerifyView):
    pass
