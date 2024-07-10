from django.shortcuts import render
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ..models import Categorys, Inputs, Salables, SubCategorys
from ..permissions import IsAdmin, IsAnonymousUser
from ..serializers.serializers_admin import *


class DefaultNumberPagination(PageNumberPagination):
    page_size = 10


@extend_schema(tags=["Admin.Categorys"])
class CategorysViewSet(ModelViewSet):
    queryset = Categorys.objects.all()
    serializer_class = CategorysSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
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
            return queryset.filter(name__icontains=category_name)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category_id",
                type=OpenApiTypes.INT,
                description="Filter by category id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                description="Filter by category name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active state",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Admin.SubCategorys"])
class SubCategorysViewSet(ModelViewSet):
    queryset = SubCategorys.objects.select_related("category").all()
    serializer_class = SubCategorysSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAnonymousUser,
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
            return queryset.filter(name__icontains=subcategory_name)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="subcategory_id",
                type=OpenApiTypes.INT,
                description="Filter by subcategory id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="subcategory",
                type=OpenApiTypes.STR,
                description="Filter by subcategory name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="category_id",
                type=OpenApiTypes.INT,
                description="Filter by category id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active state",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Admin.Inputs"])
class InputsViewSet(ModelViewSet):
    queryset = Inputs.objects.all()
    serializer_class = InputsSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Regras de query_params
        input_id = self.request.query_params.get("input_id")

        if input_id and input_id.isnumeric():
            return queryset.filter(id=input_id)

        input_name = self.request.query_params.get("input")

        if input_name:
            return queryset.filter(name__icontains=input_name)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="input_id",
                type=OpenApiTypes.INT,
                description="Filter by input id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="input",
                type=OpenApiTypes.STR,
                description="Filter by input name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active state",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                "Valid request example",
                summary='Example of request with valid "unit" field.',
                value={
                    "name": "string",
                    "price": 1.1,
                    "quantity": 1.1,
                    "unit": "kg, or g, or mg, or l, or ml, or und",
                    "subcategory": 0,
                },
                request_only=True,
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        """
        Valid values ​​for unit:
            kg; g; mg; l; ml; und
        """
        return super().create(request, *args, **kwargs)


@extend_schema(tags=["Admin.Salables"])
class SalablesViewSet(ModelViewSet):
    queryset = Salables.objects.all()
    serializer_class = SalablesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Regras de query_params
        salable_id = self.request.query_params.get("salable_id")

        if salable_id and salable_id.isnumeric():
            return queryset.filter(id=salable_id)

        salable_name = self.request.query_params.get("salable")

        if salable_name:
            return queryset.filter(name__icontains=salable_name)

        is_active_value = self.request.query_params.get("is_active")

        subcategory_id = self.request.query_params.get("subcategory_id")

        if subcategory_id and subcategory_id.isnumeric():
            return queryset.filter(id=subcategory_id)

        if is_active_value:

            if is_active_value.lower() == "false":
                is_active_value = False
                return queryset.filter(is_active=is_active_value)

            elif is_active_value.lower() == "true":
                is_active_value = True
                return queryset.filter(is_active=is_active_value)
        # Regras de query_params

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="salable_id",
                type=OpenApiTypes.INT,
                description="Filter by salable id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="salable",
                type=OpenApiTypes.STR,
                description="Filter by salable name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="subcategory_id",
                type=OpenApiTypes.INT,
                description="Filter by subcategory id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by active state",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Admin.InputsSalables"])
class InputsSalablesViewSet(ModelViewSet):
    queryset = Inputs_Salables.objects.all()
    serializer_class = InputsSalablesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()

        salable_id = self.request.query_params.get("salable_id")

        if salable_id and salable_id.isnumeric():
            return queryset.filter(id=salable_id)

        salable_name = self.request.query_params.get("salable")

        if salable_name:
            return queryset.filter(name__icontains=salable_name)

        input_id = self.request.query_params.get("input_id")

        if input_id and input_id.isnumeric():
            return queryset.filter(id=input_id)

        input_name = self.request.query_params.get("input")

        if input_name:
            return queryset.filter(name__icontains=input_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="salable_id",
                type=OpenApiTypes.INT,
                description="Filter by salable id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="salable",
                type=OpenApiTypes.STR,
                description="Filter by salable name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="input_id",
                type=OpenApiTypes.INT,
                description="Filter by input id",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="input",
                type=OpenApiTypes.STR,
                description="Filter by input name",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
