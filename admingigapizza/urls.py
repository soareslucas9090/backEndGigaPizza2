from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryListView,
    CategoryTypeCreateView,
    CategoryTypeListView,
    CustomLoginView,
    CustomLogoutView,
    MenuAdminView,
    SubcategoryCreateView,
    SubcategoryListView,
)

urlpatterns = [
    ## To registration users
    path("login/", CustomLoginView.as_view(), name="login-admin"),
    path("logout/", CustomLogoutView.as_view(), name="logout-admin"),
    ## Admin menu base
    path("menu-admin/", MenuAdminView.as_view(), name="menu-admin"),
    ## Registers
    # Types
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
    # Categories
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
    # Subcategories
    path(
        "menu-admin/register/subcategories/",
        SubcategoryListView.as_view(),
        name="list-subcategories",
    ),
    path(
        "menu-admin/register/subcategories/new/",
        SubcategoryCreateView.as_view(),
        name="create-subcategory",
    ),
]
