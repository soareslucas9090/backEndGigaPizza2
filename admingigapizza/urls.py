from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryListView,
    CategoryTypeCreateView,
    CategoryTypeListView,
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
    path(
        "menu-admin/register/types/",
        CategoryTypeListView.as_view(),
        name="list-types",
    ),
    path(
        "menu-admin/register/types/new/",
        CategoryTypeCreateView.as_view(),
        name="create-type",
    ),
]
