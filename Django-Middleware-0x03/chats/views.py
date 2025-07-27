# chats/views.py
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import MessagePagination
from .filters import MessageFilter
from .permissions import IsAdminOrModerator


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation, IsAdminOrModerator]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner] 
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['created_at']
    
class AdminOnlyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrModerator]




