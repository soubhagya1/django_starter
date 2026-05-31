from rest_framework.permissions import BasePermission
from apps.rbac.services.permission_service import has_permission


class CanCreateProduct(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "create_product")


class CanViewProduct(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "view_product")


class CanUpdateProduct(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "update_product")


class CanDeleteProduct(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "delete_product")
