from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsAdminToDocumentation(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.name == "admin2documentation"


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_admin


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        return request.user.is_superuser


class IsAnonymousUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return True

        return False


class IsNormalUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        return not request.user.is_admin
