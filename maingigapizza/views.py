from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class DefaultNumberPagination(PageNumberPagination):
    page_size = 5


class Categorys(ModelViewSet):
    queryset = Categorys.objects.all()
    serializer_class = CategorysSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class SubCategorys(ModelViewSet):
    queryset = SubCategorys.objects.select_related("category").all()
    serializer_class = SubCategorysSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class Inputs(ModelViewSet):
    queryset = Inputs.objects.all()
    serializer_class = InputsSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]


class Salables(ModelViewSet):
    queryset = Salables.objects.all()
    serializer_class = SalablesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]
