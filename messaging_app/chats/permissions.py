from rest_framework import permissions

class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsConversationParticipantAndMethodAllowed(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']  # Adjust as needed

    def has_object_permission(self, request, view, obj):
        is_participant = request.user in obj.conversation.users.all()
        method_allowed = request.method in self.SAFE_METHODS
        return is_participant and method_allowed


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit it.
    Assumes the object has a 'user' or 'owner' attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to owner only
        return obj.user == request.user
