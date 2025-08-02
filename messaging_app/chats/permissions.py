from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    

    def has_permission(self, request, view):
        # Basic check
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Apply for read, update, delete
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'conversation'):
                # obj is a Message
                return request.user in obj.conversation.participants.all()
            elif hasattr(obj, 'participants'):
                # obj is a Conversation
                return request.user in obj.participants.all()
        return False