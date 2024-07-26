from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from maingigapizza.models import Categories, CategoryTypes

from .forms import CategoryForm, CategoryTypeForm, CustomAuthenticationForm
from .permissions import IsAdmin


@method_decorator(csrf_protect, name="dispatch")
class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = "registration/login.html"


@method_decorator(csrf_protect, name="dispatch")
class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login-admin")


def isAdmin(request, toRender):
    if IsAdmin().has_permission(request=request, view=None):
        context = None
        if len(toRender) > 1:
            context = toRender[1]
        return render(request=request, template_name=toRender[0], context=context)
    else:
        return redirect("login-admin")


@method_decorator(csrf_protect, name="dispatch")
class MenuAdminView(View):
    def get(self, request):
        return isAdmin(request, ["menu_admin/base_menu.html"])


@method_decorator(csrf_protect, name="dispatch")
class CategoryTypeListView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            types = CategoryTypes.objects.filter(name__icontains=query).order_by("name")
        else:
            types = CategoryTypes.objects.all().order_by("name")

        return isAdmin(
            request,
            [
                "menu_admin/registers/types/list_types.html",
                {"types": types},
            ],
        )

    def post(self, request):
        type_id = request.POST.get("type_id")
        if type_id:
            type = get_object_or_404(CategoryTypes, id=type_id)
            type.is_active = not type.is_active
        else:
            new_name = request.POST.get("type_name")
            type_id = request.POST.get("type_name_id")
            type = get_object_or_404(Categories, id=type_id)
            type.name = new_name

        type.save()
        return redirect("list-types")


@method_decorator(csrf_protect, name="dispatch")
class CategoryTypeCreateView(View):
    def get(self, request):
        form = CategoryTypeForm()
        return isAdmin(
            request,
            ["menu_admin/registers/types/create_type.html", {"form": form}],
        )

    def post(self, request):
        form = CategoryTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list-types")
        return isAdmin(request, ["admin/forms/types/create_type.html", {"form": form}])


@method_decorator(csrf_protect, name="dispatch")
class CategoryListView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            categories = Categories.objects.filter(name__icontains=query).order_by(
                "name"
            )
        else:
            categories = Categories.objects.all().order_by("name")

        return isAdmin(
            request,
            [
                "menu_admin/registers/categories/list_categories.html",
                {"categories": categories},
            ],
        )

    def post(self, request):
        category_id = request.POST.get("category_id")
        if category_id:
            category = get_object_or_404(Categories, id=category_id)
            category.is_active = not category.is_active
        else:
            new_name = request.POST.get("category_name")
            category_id = request.POST.get("category_name_id")
            category = get_object_or_404(Categories, id=category_id)
            category.name = new_name

        category.save()
        return redirect("list-categories")


@method_decorator(csrf_protect, name="dispatch")
class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return isAdmin(
            request,
            ["menu_admin/registers/categories/create_category.html", {"form": form}],
        )

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list-categories")
        return isAdmin(
            request, ["admin/forms/categories/create_category.html", {"form": form}]
        )
