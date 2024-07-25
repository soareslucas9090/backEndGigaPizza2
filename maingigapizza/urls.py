from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.views_admin import (
    CategoriesViewSet,
    CategoryTypesViewSet,
    InputsViewSet,
    SalablesCompositionsViewSet,
    SalablesViewSet,
    SubCategoriesViewSet,
)
from .views.views_public import CreateUserViewSet, ListSalablesViewSet

gigapizza_router_admin = SimpleRouter()
gigapizza_router_admin.register(r"types", CategoryTypesViewSet, basename="admin-types")
gigapizza_router_admin.register(
    r"categories", CategoriesViewSet, basename="admin-categories"
)
gigapizza_router_admin.register(
    r"subcategories", SubCategoriesViewSet, basename="admin-subcategories"
)
gigapizza_router_admin.register(r"inputs", InputsViewSet, basename="admin-inputs")
gigapizza_router_admin.register(r"salables", SalablesViewSet, basename="admin-salables")
gigapizza_router_admin.register(
    r"salables_compositions",
    SalablesCompositionsViewSet,
    basename="admin-salables_compositions",
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
