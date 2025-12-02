from rest_framework import permissions


class IsAdminOrManagerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS
             and request.user.is_authenticated)
            or request.user.is_authenticated
            and (request.user.is_staff
                 or request.user.employee.is_director()
                 or request.user.employee.is_deputy_director()
                 or request.user.employee.is_head_department()
                 or request.user.employee.is_deputy_head_department())
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS
             and (request.user.is_staff
                  or request.user.employee in obj.executors.all()))
            or request.user.is_staff
            or request.user.employee.is_director()
            or obj.initiator == request.user.employee
        )
