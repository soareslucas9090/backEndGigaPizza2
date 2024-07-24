from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from .forms import CustomAuthenticationForm
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
