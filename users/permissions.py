from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return request.user.role.name == 'manager'


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role.name == 'admin'
