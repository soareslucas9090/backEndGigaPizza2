from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

gigapizza_router = SimpleRouter()
gigapizza_router.register("categorys", Categorys)
gigapizza_router.register("subcategorys", SubCategorys)
gigapizza_router.register("inputs", Inputs)
gigapizza_router.register("salables", Salables)
gigapizza_router.register("inputs_salables", InputsSalables)
gigapizza_router.register("pizzas", Pizzas)

urlpatterns = [
    path("v1/", include(gigapizza_router.urls)),
]
