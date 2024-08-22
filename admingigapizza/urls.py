from django.urls import path

from .views import (
    CategoryListView,
    CategoryTypeListView,
    CustomLoginView,
    CustomLogoutView,
    InputListView,
    MenuAdminView,
    SalableCompositionCreateView,
    SalableCompositionDetailView,
    SalableCompositionListView,
    SalableCreateView,
    SalableListView,
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
    # Categories
    path(
        "menu-admin/register/categories/",
        CategoryListView.as_view(),
        name="list-categories",
    ),
    # Subcategories
    path(
        "menu-admin/register/subcategories/",
        SubcategoryListView.as_view(),
        name="list-subcategories",
    ),
    # Inputs
    path(
        "menu-admin/register/inputs/",
        InputListView.as_view(),
        name="list-inputs",
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
    # Compositions
    path(
        "menu-admin/register/compositions/",
        SalableCompositionListView.as_view(),
        name="list-composition",
    ),
    path(
        "menu-admin/register/compositions/detail/",
        SalableCompositionDetailView.as_view(),
        name="detail-composition",
    ),
    path(
        "menu-admin/register/compositions/new/",
        SalableCompositionCreateView.as_view(),
        name="create-composition",
    ),
]
