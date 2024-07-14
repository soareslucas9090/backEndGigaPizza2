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
    r"categories", CategorysViewSet, basename="admin-categories"
)
gigapizza_router_admin.register(
    r"subcategories", SubCategorysViewSet, basename="admin-subcategories"
)
gigapizza_router_admin.register(r"inputs", InputsViewSet, basename="admin-inputs")
gigapizza_router_admin.register(r"salables", SalablesViewSet, basename="admin-salables")
gigapizza_router_admin.register(
    r"inputs_salables", InputsSalablesViewSet, basename="admin-inputs_salables"
)

gigapizza_router_public = SimpleRouter()
gigapizza_router_public.register(
    r"create_user", CreateUserViewSet, basename="public-create_user"
)
gigapizza_router_public.register(
    r"list_salables", ListSalablesViewSet, basename="public-list_salables"
)

urlpatterns = [
    path(r"v1/admin/", include(gigapizza_router_admin.urls)),
    path(r"v1/public/", include(gigapizza_router_public.urls)),
]
