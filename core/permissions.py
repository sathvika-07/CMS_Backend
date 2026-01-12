from rest_framework.permissions import BasePermission, SAFE_METHODS


class StaffWritePermission(BasePermission):
    """Allow read to anyone; write only to staff/admin users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)
