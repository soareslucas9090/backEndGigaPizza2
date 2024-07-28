from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from maingigapizza.models import (
    Categories,
    CategoryTypes,
    Inputs,
    Salables,
    SubCategories,
)

from .forms import (
    CategoryForm,
    CategoryTypeForm,
    CustomAuthenticationForm,
    InputForm,
    SubCategoryForm,
)
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

        return isAdmin(
            request, ["menu_admin/registers/types/create_type.html", {"form": form}]
        )


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
            request,
            ["menu_admin/registers/categories/create_category.html", {"form": form}],
        )


@method_decorator(csrf_protect, name="dispatch")
class SubcategoryListView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            subcategories = SubCategories.objects.filter(
                name__icontains=query
            ).order_by("name")
        else:
            subcategories = SubCategories.objects.all().order_by("name")

        return isAdmin(
            request,
            [
                "menu_admin/registers/subcategories/list_subcategories.html",
                {"subcategories": subcategories},
            ],
        )

    def post(self, request):
        subcategory_id = request.POST.get("subcategory_id")
        if subcategory_id:
            subcategory = get_object_or_404(SubCategories, id=subcategory_id)
            subcategory.is_active = not subcategory.is_active
        else:
            new_name = request.POST.get("subcategory_name")
            subcategory_id = request.POST.get("subcategory_name_id")
            subcategory = get_object_or_404(SubCategories, id=subcategory_id)
            subcategory.name = new_name

        subcategory.save()
        return redirect("list-subcategories")


@method_decorator(csrf_protect, name="dispatch")
class SubcategoryCreateView(View):
    def get(self, request):
        edit_id = request.GET.get("edit_id")

        if edit_id:
            subcategory = get_object_or_404(SubCategories, id=edit_id)
            form = SubCategoryForm(
                instance=subcategory, category_type=subcategory.category.type
            )
        else:
            form = SubCategoryForm()

        return isAdmin(
            request,
            [
                "menu_admin/registers/subcategories/create_subcategory.html",
                {"form": form},
            ],
        )

    def post(self, request):
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            edit_id = request.POST.get("edit_id")
            if edit_id:
                subcategory = get_object_or_404(SubCategories, id=edit_id)
                form = SubCategoryForm(request.POST, instance=subcategory)
                if form.is_valid():
                    form.save()
                    return redirect("list-subcategories")

            form.save()
            return redirect("list-subcategories")

        constraint_error = "Sub categories com este Name e Category já existe."
        errors = str(form.non_field_errors())

        if constraint_error in errors:
            form.errors.clear()
            form.add_error(
                None,
                "Já existe uma subcategoria criada com este nome e esta categoria.",
            )

        return isAdmin(
            request,
            [
                "menu_admin/registers/subcategories/create_subcategory.html",
                {"form": form},
            ],
        )


@method_decorator(csrf_protect, name="dispatch")
class InputListView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            inputs = Inputs.objects.filter(name__icontains=query).order_by("name")
        else:
            inputs = Inputs.objects.all().order_by("name")

        return isAdmin(
            request,
            [
                "menu_admin/registers/inputs/list_inputs.html",
                {"inputs": inputs},
            ],
        )

    def post(self, request):
        input_id = request.POST.get("input_id")
        if input_id:
            input = get_object_or_404(Inputs, id=input_id)
            input.is_active = not input.is_active

        elif request.POST.get("input_name"):
            new_name = request.POST.get("input_name")
            input_id = request.POST.get("input_name_id")
            input = get_object_or_404(Inputs, id=input_id)
            input.name = new_name

        elif request.POST.get("input_price"):
            new_price = request.POST.get("input_price")
            input_id = request.POST.get("input_price_id")
            input = get_object_or_404(Inputs, id=input_id)
            input.price = new_price

        elif request.POST.get("input_quantity"):
            new_quantity = request.POST.get("input_quantity")
            input_id = request.POST.get("input_quantity_id")
            input = get_object_or_404(Inputs, id=input_id)
            input.quantity = new_quantity

        input.save()
        return redirect("list-inputs")


@method_decorator(csrf_protect, name="dispatch")
class InputCreateView(View):
    def get(self, request):
        edit_id = request.GET.get("edit_id")

        if edit_id:
            input = get_object_or_404(Inputs, id=edit_id)
            form = InputForm(instance=input)
        else:
            form = InputForm()

        return isAdmin(
            request,
            [
                "menu_admin/registers/inputs/create_input.html",
                {"form": form},
            ],
        )

    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            edit_id = request.POST.get("edit_id")
            if edit_id:
                input = get_object_or_404(Inputs, id=edit_id)
                form = InputForm(request.POST, instance=input)
                if form.is_valid():
                    form.save()
                    return redirect("list-inputs")

            form.save()
            return redirect("list-inputs")

        constraint_error = "Inputs com este Name e Subcategory já existe"
        errors = str(form.non_field_errors())

        if constraint_error in errors:
            form.errors.clear()
            form.add_error(
                None, "Já existe um insumo criado com este nome e esta subcategoria."
            )

        return isAdmin(
            request,
            ["menu_admin/registers/inputs/create_input.html", {"form": form}],
        )
