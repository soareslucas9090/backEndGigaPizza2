from django.urls import path

from .views import CustomLoginView, CustomLogoutView, MenuAdminView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login-admin"),
    path("menu-admin/", MenuAdminView.as_view(), name="menu-admin"),
    path("logout/", CustomLogoutView.as_view(), name="logout-admin"),
]
