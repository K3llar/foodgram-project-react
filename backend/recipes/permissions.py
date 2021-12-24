from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class AuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
                request.user.is_admin or
                obj.author == request.user or request.method == 'POST'):
            return True
        return request.method in permissions.SAFE_METHODS
