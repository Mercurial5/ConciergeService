from rest_framework.permissions import BasePermission


class IsRelated(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        return False
