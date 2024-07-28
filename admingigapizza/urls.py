from django.urls import path

from .views import (
    CategoryCreateView,
    CategoryListView,
    CategoryTypeCreateView,
    CategoryTypeListView,
    CustomLoginView,
    CustomLogoutView,
    InputCreateView,
    InputListView,
    MenuAdminView,
    SalableCreateView,
    SalableListView,
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
    # Inputs
    path(
        "menu-admin/register/inputs/",
        InputListView.as_view(),
        name="list-inputs",
    ),
    path(
        "menu-admin/register/inputs/new/",
        InputCreateView.as_view(),
        name="create-input",
    ),
    # Salables
    path(
        "menu-admin/register/salables/",
        SalableListView.as_view(),
        name="list-salables",
    ),
    path(
        "menu-admin/register/salables/new/",
        SalableCreateView.as_view(),
        name="create-salable",
    ),
]
