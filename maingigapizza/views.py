from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
        IsAuthenticatedOrReadOnly,
    ]
    http_method_names = ["get", "head", "patch", "delete", "post"]
