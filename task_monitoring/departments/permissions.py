from rest_framework import permissions


class IsAdminOrDirectorOrCurrentUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS
             and request.user.is_authenticated)
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS
             and (request.user.is_staff
                  or obj.user == request.user))
            or request.user.is_staff
        )