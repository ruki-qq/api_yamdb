from rest_framework import permissions


class IsAuthenticatedAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Permission to only allow owner of an object to change it."""

    def has_object_permission(self, request, view, obj):
        # Maybe need to add comments logic
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsModerator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        # Maybe need to add comments logic
        # Add permissions to delete reviews and comments
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(permissions.AllowAny):
    # 99% useless perm, might delete in future
    pass
