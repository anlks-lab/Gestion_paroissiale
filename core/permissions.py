from rest_framework.permissions import BasePermission

SECRETARY_ROLES = {"secretaire", "tresorier", "responsable", "pretre", "admin"}
TREASURER_ROLES = {"tresorier", "pretre", "admin"}
ADMIN_ROLES = {"admin"}


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ADMIN_ROLES)


class IsSecretaryOrAbove(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in SECRETARY_ROLES)


class IsTreasurerOrAbove(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in TREASURER_ROLES)
