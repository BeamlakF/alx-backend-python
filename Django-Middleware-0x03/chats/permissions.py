from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assuming the model instance has a user field
        return obj.user == request.user

class IsParticipantOfConversation(BasePermission):
    

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Assuming 'obj' is a Message or Conversation instance
        return request.user in obj.participants.all()  # or adjust per your model
    
class IsAdminOrModerator(permissions.BasePermission):
    """
    Custom permission to only allow users with 'admin' or 'moderator' role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in ['admin', 'moderator']
        )