from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or 
            request.user.is_authenticated and 
            (request.user.is_admin or obj.user == request.user)
        )
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS → allow for all
        if request.method in SAFE_METHODS:
            return True
        # For POST, PUT, DELETE → only admin allowed
        return request.user and request.user.is_staff
