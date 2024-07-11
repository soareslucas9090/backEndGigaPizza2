from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.views_admin import (
    CategorysViewSet,
    InputsSalablesViewSet,
    InputsViewSet,
    SalablesViewSet,
    SubCategorysViewSet,
)
from .views.views_public import CreateUserViewSet, ListSalablesViewSet

gigapizza_router_admin = SimpleRouter()
gigapizza_router_admin.register(
    "categorys", CategorysViewSet, basename="admin-categorys"
)
gigapizza_router_admin.register(
    "subcategorys", SubCategorysViewSet, basename="admin-subcategorys"
)
gigapizza_router_admin.register("inputs", InputsViewSet, basename="admin-inputs")
gigapizza_router_admin.register("salables", SalablesViewSet, basename="admin-salables")
gigapizza_router_admin.register(
    "inputs_salables", InputsSalablesViewSet, basename="admin-inputs_salables"
)

gigapizza_router_public = SimpleRouter()
gigapizza_router_public.register(
    "create_user", CreateUserViewSet, basename="public-create_user"
)
gigapizza_router_public.register(
    "list_salables", ListSalablesViewSet, basename="public-list_salables"
)

urlpatterns = [
    path("v1/admin/", include(gigapizza_router_admin.urls)),
    path("v1/public/", include(gigapizza_router_public.urls)),
]
