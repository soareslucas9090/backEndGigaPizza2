from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

gigapizza_router = SimpleRouter()
gigapizza_router.register("categorys", Categorys)

urlpatterns = [
    path("v1/", include(gigapizza_router.urls)),
]
