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

    def clean_name(self):
        name = self.cleaned_data["name"]
        if CategoryTypes.objects.filter(name__iexact=name.lower()).exists():
            raise forms.ValidationError("Já existe um tipo de categoria com este nome.")
        return name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name", "type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["type"].queryset = CategoryTypes.objects.filter(is_active=True)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Categories.objects.filter(name__iexact=name.lower()).exists():
            raise forms.ValidationError("Já existe uma categoria com este nome e tipo.")
        return name


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

    def clean_name(self):
        name = self.cleaned_data["name"]
        if SubCategories.objects.filter(name__iexact=name.lower()).exists():
            raise forms.ValidationError(
                "Já existe uma subcategoria com este nome e categoria."
            )
        return name


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

    def clean_name(self):
        name = self.cleaned_data["name"]
        print(self.cleaned_data)
        if Inputs.objects.filter(name__iexact=name.lower()).exists():
            raise forms.ValidationError(
                "Já existe um insumo com este nome e subcategoria."
            )
        return name


class SalableForm(forms.ModelForm):
    class Meta:
        model = Salables
        fields = ["name", "description", "price", "subcategory"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subcategory"].queryset = SubCategories.objects.filter(
            category__type__name="P/ Venda", is_active=True
        )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Salables.objects.filter(name__iexact=name.lower()).exists():
            raise forms.ValidationError(
                "Já existe item p/ venda com este nome e subcategoria."
            )
        return name


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
