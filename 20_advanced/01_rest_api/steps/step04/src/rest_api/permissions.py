from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow read to anyone; write only to the record owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
