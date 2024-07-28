from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from ..models import Salables, Users
from ..permissions import IsAnonymousUser
from ..serializers.serializers_public import SalablesPublicSerializer, UsersSerializer


@method_decorator(csrf_protect, name="dispatch")
class RedirectUserView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect("menu-admin")
            else:
                return redirect("login-admin")
        else:
            return redirect("login-admin")


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
    serializer_class = SalablesPublicSerializer
    pagination_class = ListItensNumberPagination
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = Salables.objects.filter(
            is_active=True,
            subcategory__isactive=True,
            subcategory__category__isactive=True,
        )

        return queryset.order_by("subcategory")
