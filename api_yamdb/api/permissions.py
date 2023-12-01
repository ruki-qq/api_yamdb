from rest_framework import permissions


def is_admin(user):
    return user.is_authenticated and (
        user.is_superuser or user.role == 'admin'
    )


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Anonymous user can read.
    Authenticated user can create.
    Owner or Moderator and above can change.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or is_admin(request.user)
            or request.user.role == 'moderator'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Only Admin can create or change."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or is_admin(
            request.user
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or is_admin(
            request.user
        )
