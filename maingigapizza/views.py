from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class DefaultNumberPagination(PageNumberPagination):
    page_size = 10


class Categorys(ModelViewSet):
    queryset = Categorys.objects.all()
    serializer_class = CategorysSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Regras de query_params
        category_id = self.request.query_params.get("category_id")

        if category_id and category_id.isnumeric():
            return queryset.filter(id=category_id)

        category_name = self.request.query_params.get("category")

        if category_name:
            return queryset.filter(name=category_name)

        is_active_value = self.request.query_params.get("is_active")

        if is_active_value:

            if is_active_value.lower() == "false":
                is_active_value = False
                return queryset.filter(is_active=is_active_value)

            elif is_active_value.lower() == "true":
                is_active_value = True
                return queryset.filter(is_active=is_active_value)
        # Regras de query_params

        return queryset


class SubCategorys(ModelViewSet):
    queryset = SubCategorys.objects.select_related("category").all()
    serializer_class = SubCategorysSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Regras de query_params
        subcategory_id = self.request.query_params.get("subcategory_id")

        if subcategory_id and subcategory_id.isnumeric():
            return queryset.filter(id=subcategory_id)

        subcategory_name = self.request.query_params.get("subcategory")

        if subcategory_name:
            return queryset.filter(name=subcategory_name)

        category_id = self.request.query_params.get("category_id")

        if category_id and category_id.isnumeric():
            return queryset.filter(category=category_id)

        is_active_value = self.request.query_params.get("is_active")

        if is_active_value:

            if is_active_value.lower() == "false":
                is_active_value = False
                return queryset.filter(is_active=is_active_value)

            elif is_active_value.lower() == "true":
                is_active_value = True
                return queryset.filter(is_active=is_active_value)
        # Regras de query_params

        return queryset


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


class InputsSalables(ModelViewSet):
    queryset = Inputs_Salables.objects.all()
    serializer_class = InputsSalablesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.request.query_params)
        return queryset
