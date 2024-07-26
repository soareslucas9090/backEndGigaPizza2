from django import forms
from django.contrib.auth.forms import AuthenticationForm

from maingigapizza.models import Categories, CategoryTypes, SubCategories


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


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategories
        fields = ["name", "category"]
