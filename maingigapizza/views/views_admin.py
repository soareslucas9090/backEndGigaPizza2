from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import (
    Categories,
    CategoryTypes,
    Inputs,
    Salables,
    Salables_Compositions,
    SubCategories,
)
from ..permissions import IsAdmin, IsAdminToDocumentation, IsAnonymousUser
from ..serializers.serializers_admin import (
    CategoriesSerializer,
    CategoryTypesSerializer,
    InputsSerializer,
    SalablesCompositionsSerializer,
    SalablesSerializer,
    SubCategoriesSerializer,
)


class DefaultNumberPagination(PageNumberPagination):
    page_size = 10


@extend_schema(tags=["Admin.CategoriesTypes"])
class CategoryTypesViewSet(ModelViewSet):
    queryset = CategoryTypes.objects.all()
    serializer_class = CategoryTypesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset().order_by("name")

        # Regras de query_params

        type_name = self.request.query_params.get("type")

        if type_name:
            return queryset.filter(name__icontains=type_name)

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
                name="type",
                type=OpenApiTypes.STR,
                description="Filter by category type name",
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
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        serializer_hateoas = {"category_types": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                for i in range(len(serializer_hateoas["category_types"])):
                    del serializer_hateoas["category_types"][i]["links"]

        return self.get_paginated_response(serializer_hateoas)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_hateoas = {"category_type": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                del serializer_hateoas["category_type"]["links"]

        return Response(serializer_hateoas)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            permission = IsAdminToDocumentation()
            if permission.has_permission(self.request, self):
                raise PermissionDenied()

        return super().get_permissions()


@extend_schema(tags=["Admin.Categories"])
class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset().order_by("name")

        # Regras de query_params

        category_name = self.request.query_params.get("category")

        if category_name:
            return queryset.filter(name__icontains=category_name)

        type_id = self.request.query_params.get("type_id")

        if type_id and type_id.isnumeric():
            return queryset.filter(type=type_id)

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
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        serializer_hateoas = {"categories": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                for i in range(len(serializer_hateoas["categories"])):
                    del serializer_hateoas["categories"][i]["links"]

        return self.get_paginated_response(serializer_hateoas)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_hateoas = {"category": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                del serializer_hateoas["category"]["links"]

        return Response(serializer_hateoas)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            permission = IsAdminToDocumentation()
            if permission.has_permission(self.request, self):
                raise PermissionDenied()

        return super().get_permissions()


@extend_schema(tags=["Admin.SubCategories"])
class SubCategoriesViewSet(ModelViewSet):
    queryset = SubCategories.objects.select_related("category").all()
    serializer_class = SubCategoriesSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset().order_by("name")

        # Regras de query_params

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
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        serializer_hateoas = {"subcategories": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                for i in range(len(serializer_hateoas["subcategories"])):
                    del serializer_hateoas["subcategories"][i]["links"]

        return self.get_paginated_response(serializer_hateoas)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_hateoas = {"subcategory": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                del serializer_hateoas["subcategories"]["links"]

        return Response(serializer_hateoas)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            permission = IsAdminToDocumentation()
            if permission.has_permission(self.request, self):
                raise PermissionDenied()

        return super().get_permissions()


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
        queryset = super().get_queryset().order_by("name")

        # Regras de query_params

        input_name = self.request.query_params.get("input")

        if input_name:
            return queryset.filter(name__icontains=input_name)

        subcategory_id = self.request.query_params.get("subcategory_id")

        if subcategory_id and subcategory_id.isnumeric():
            return queryset.filter(subcategory=subcategory_id)

        category_id = self.request.query_params.get("category_id")

        if category_id and category_id.isnumeric():
            return queryset.filter(subcategory__category=category_id)

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
                name="input",
                type=OpenApiTypes.STR,
                description="Filter by input name",
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
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        serializer_hateoas = {"inputs": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                for i in range(len(serializer_hateoas["inputs"])):
                    del serializer_hateoas["inputs"][i]["links"]

        return self.get_paginated_response(serializer_hateoas)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_hateoas = {"input": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                del serializer_hateoas["inputs"]["links"]
        return Response(serializer_hateoas)

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

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            permission = IsAdminToDocumentation()
            if permission.has_permission(self.request, self):
                raise PermissionDenied()

        return super().get_permissions()


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
        queryset = super().get_queryset().order_by("name")

        # Regras de query_params

        salable_name = self.request.query_params.get("salable")

        if salable_name:
            return queryset.filter(name__icontains=salable_name)

        is_active_value = self.request.query_params.get("is_active")

        subcategory_id = self.request.query_params.get("subcategory_id")

        if subcategory_id and subcategory_id.isnumeric():
            return queryset.filter(subcategory=subcategory_id)

        category_id = self.request.query_params.get("category_id")

        if category_id and category_id.isnumeric():
            return queryset.filter(subcategory__category=category_id)

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
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        serializer_hateoas = {"salables": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                for i in range(len(serializer_hateoas["salables"])):
                    del serializer_hateoas["salables"][i]["links"]

        return self.get_paginated_response(serializer_hateoas)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_hateoas = {"salable": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                del serializer_hateoas["salables"]["links"]
        return Response(serializer_hateoas)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            permission = IsAdminToDocumentation()
            if permission.has_permission(self.request, self):
                raise PermissionDenied()

        return super().get_permissions()


@extend_schema(tags=["Admin.SalablesCompositions"])
class SalablesCompositionsViewSet(ModelViewSet):
    queryset = Salables_Compositions.objects.all()
    serializer_class = SalablesCompositionsSerializer
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAdmin,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")

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
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        serializer_hateoas = {"salables_compositions": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                for i in range(len(serializer_hateoas["salables_compositions"])):
                    del serializer_hateoas["salables_compositions"][i]["links"]

        return self.get_paginated_response(serializer_hateoas)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="links",
                type=OpenApiTypes.BOOL,
                description="Show or not show links from the HATEOAS method (choose false for a lighter answer, but without links)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_hateoas = {"salables_compositions": serializer.data}
        links = self.request.query_params.get("links")

        if links:
            if links.lower() == "false":
                links = False
                del serializer_hateoas["salables_compositions"]["links"]
        return Response(serializer_hateoas)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE", "POST"]:
            permission = IsAdminToDocumentation()
            if permission.has_permission(self.request, self):
                raise PermissionDenied()

        return super().get_permissions()
