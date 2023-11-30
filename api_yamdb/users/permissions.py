from rest_framework import permissions


class IsUser(permissions.IsAuthenticatedOrReadOnly):
    """Permission to only allow owner of an object to change it."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated


class IsModerator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        # Maybe need to add comments logic
        # Add permissions to delete reviews and comments
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )
