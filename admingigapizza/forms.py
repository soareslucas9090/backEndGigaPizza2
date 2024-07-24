from django import forms
from django.contrib.auth.forms import AuthenticationForm

from maingigapizza.models import Categorys


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categorys
        fields = ["name"]
