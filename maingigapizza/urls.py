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
gigapizza_router_admin.register("categorys", CategorysViewSet)
gigapizza_router_admin.register("subcategorys", SubCategorysViewSet)
gigapizza_router_admin.register("inputs", InputsViewSet)
gigapizza_router_admin.register("salables", SalablesViewSet)
gigapizza_router_admin.register("inputs_salables", InputsSalablesViewSet)

gigapizza_router_public = SimpleRouter()
gigapizza_router_public.register("create_user", CreateUserViewSet)
gigapizza_router_public.register("list_salables", ListSalablesViewSet)

urlpatterns = [
    path("v1/admin/", include(gigapizza_router_admin.urls)),
    path("v1/public/", include(gigapizza_router_public.urls)),
]
