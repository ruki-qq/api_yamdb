from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Permission to give access to users with moderator role."""

    ROLE = 'admin'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == self.ROLE)
        )
