from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsAdminToDocumentation(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.email == "admin2documentation@gigapizza.com"


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_admin
