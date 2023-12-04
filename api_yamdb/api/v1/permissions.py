from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Anonymous user can read.
    Authenticated user can create.
    Owner or Moderator and above can change.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Only Admin can create or change."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    """Permission to give access to users with admin role."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
