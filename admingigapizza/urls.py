from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryListView,
    CustomLoginView,
    CustomLogoutView,
    MenuAdminView,
)

urlpatterns = [
    ## To registration users
    path("login/", CustomLoginView.as_view(), name="login-admin"),
    path("logout/", CustomLogoutView.as_view(), name="logout-admin"),
    ## Admin menu base
    path("menu-admin/", MenuAdminView.as_view(), name="menu-admin"),
    ## Registers
    path(
        "menu-admin/register/categories/",
        CategoryListView.as_view(),
        name="list-categories",
    ),
    path(
        "menu-admin/register/categories/new/",
        CategoryCreateView.as_view(),
        name="create-category",
    ),
]
