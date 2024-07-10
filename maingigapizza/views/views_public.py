from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ..models import Users
from ..permissions import IsAnonymousUser
from ..serializers.serializers_admin import *


class DefaultNumberPagination(PageNumberPagination):
    page_size = 10


@extend_schema(tags=["Admin.Categorys"])
class CreateUserViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = Users
    pagination_class = DefaultNumberPagination
    permission_classes = [
        IsAnonymousUser,
    ]
    http_method_names = ["post"]
