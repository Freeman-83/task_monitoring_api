from rest_framework import permissions


class IsAdminOrExecutor(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS
                 and request.user.is_authenticated)
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS
                 and obj.responsible_executor == request.user)
                or request.user.is_staff)


# class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):

#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_staff
#                 or obj.author == request.user)
