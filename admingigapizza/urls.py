from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import CustomLogoutView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login-admin"),
    path("logout/", CustomLogoutView.as_view(), name="logout-admin"),
]
