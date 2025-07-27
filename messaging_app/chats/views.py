from django.shortcuts import render

from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        # Automatically associate the sender as the current user if needed
        serializer.save(sender=self.request.user)
from rest_framework.permissions import IsAuthenticated

class MessageViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAuthenticated]
