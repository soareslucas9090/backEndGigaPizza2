from django import forms
from django.contrib.auth.forms import AuthenticationForm

from maingigapizza.models import (
    Categories,
    CategoryTypes,
    Inputs,
    Salables,
    Salables_Compositions,
    SubCategories,
)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class CategoryTypeForm(forms.ModelForm):
    class Meta:
        model = CategoryTypes
        fields = ["name"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name", "type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].queryset = CategoryTypes.objects.filter(is_active=True)


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategories
        fields = ["name", "category"]

    def __init__(self, *args, **kwargs):
        category_type = kwargs.pop("category_type", None)
        super().__init__(*args, **kwargs)
        if category_type is not None:
            self.fields["category"].queryset = Categories.objects.filter(
                type=category_type, is_active=True
            )


class InputForm(forms.ModelForm):
    class Meta:
        model = Inputs
        fields = ["name", "price", "quantity", "unit", "subcategory"]
        widgets = {"unit": forms.Select(choices=Inputs.UNITS)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subcategory"].queryset = SubCategories.objects.filter(
            category__type__name="Insumos", is_active=True
        )


class SalableForm(forms.ModelForm):
    class Meta:
        model = Salables
        fields = ["name", "description", "price", "subcategory"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subcategory"].queryset = SubCategories.objects.filter(
            category__type__name="P/ Venda", is_active=True
        )


class SalablesCompositionForm(forms.ModelForm):
    class Meta:
        model = Salables_Compositions
        fields = ["salable", "input", "quantity"]

    def __init__(self, *args, **kwargs):
        salable_id = kwargs.pop("salable_id", None)
        super().__init__(*args, **kwargs)

        inputs = Inputs.objects.filter(is_active=True)
        self.fields["input"].widget = forms.Select(
            choices=[(input.id, f"{input.name} - {input.unit}") for input in inputs]
        )

        if salable_id is not None:
            self.fields["salable"].initial = salable_id
