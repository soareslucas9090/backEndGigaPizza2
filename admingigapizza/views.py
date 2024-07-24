from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from maingigapizza.models import Categorys

from .forms import CategoryForm, CustomAuthenticationForm
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
class CategoryListView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            categories = Categorys.objects.filter(name__icontains=query).order_by(
                "name"
            )
        else:
            categories = Categorys.objects.all().order_by("name")

        return isAdmin(
            request,
            ["menu_admin/registers/list_categories.html", {"categories": categories}],
        )

    def post(self, request):
        category_id = request.POST.get("category_id")
        if category_id:
            category = get_object_or_404(Categorys, id=category_id)
            category.is_active = not category.is_active
        else:
            new_name = request.POST.get("category_name")
            category_id = request.POST.get("category_name_id")
            category = get_object_or_404(Categorys, id=category_id)
            category.name = new_name

        category.save()
        return redirect("list-categories")


@method_decorator(csrf_protect, name="dispatch")
class CategoryCreateView(View):
    def get(self, request):
        form = CategoryForm()
        return isAdmin(
            request, ["menu_admin/registers/create_category.html", {"form": form}]
        )

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list-categories")
        return isAdmin(request, ["admin/forms/create_category.html", {"form": form}])
