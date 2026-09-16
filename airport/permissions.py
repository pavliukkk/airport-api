from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.user.is_authenticated
                and request.method in SAFE_METHODS
                and request.user
            )
            or (request.user.is_staff and request.user)
        )
