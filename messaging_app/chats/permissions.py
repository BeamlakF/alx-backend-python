from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Make sure user is authenticated (already enforced globally)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj will be a Message or a Conversation
        """
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False
