from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from maingigapizza.views.views_public import RedirectUserView

from .views_jwt import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("", RedirectView.as_view(url="/api/schema/swagger/", permanent=True)),
    path("admin/", admin.site.urls),
    path("api/maingigapizza/", include("maingigapizza.urls")),
    path("redirect/", RedirectUserView.as_view(), name="redirect-login"),
    path("app/admin/", include("admingigapizza.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("__debug__/", include("debug_toolbar.urls")),
]
