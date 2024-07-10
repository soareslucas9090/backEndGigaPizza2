from pathlib import Path

from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import Salables, Users
from ..permissions import IsAnonymousUser
from ..serializers.serializers_public import SalablesSerializer, UsersSerializer


class ListItensNumberPagination(PageNumberPagination):
    page_size = 100


@extend_schema(tags=["Public.Create Users"])
class CreateUserViewSet(GenericViewSet, CreateModelMixin):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [
        IsAnonymousUser,
    ]
    http_method_names = ["post"]


@extend_schema(tags=["Public.Salables"])
class ListSalablesViewSet(GenericViewSet, ListModelMixin):
    queryset = Salables.objects.all()
    serializer_class = SalablesSerializer
    pagination_class = ListItensNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        print("===== Aqui")
        dir = Path(__file__).resolve().parent.parent.parent
        serializer = self.get_serializer(self.get_queryset(), many=True)
        retorno = {"teste": f"{dir}"}
        return Response(retorno, status=status.HTTP_200_OK)
