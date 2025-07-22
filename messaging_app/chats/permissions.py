from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit it.
    Assumes the object has a 'user' or 'owner' attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to owner only
        return obj.user == request.user
