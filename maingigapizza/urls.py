from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.views_admin import (
    CategorysViewSet,
    InputsSalablesViewSet,
    InputsViewSet,
    PizzasViewSet,
    SalablesViewSet,
    SubCategorysViewSet,
)

gigapizza_router = SimpleRouter()
gigapizza_router.register("categorys", CategorysViewSet)
gigapizza_router.register("subcategorys", SubCategorysViewSet)
gigapizza_router.register("inputs", InputsViewSet)
gigapizza_router.register("salables", SalablesViewSet)
gigapizza_router.register("inputs_salables", InputsSalablesViewSet)
gigapizza_router.register("pizzas", PizzasViewSet)

urlpatterns = [
    path("v1/", include(gigapizza_router.urls)),
]
