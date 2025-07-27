from rest_framework import serializers
from .models import User, Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    # Explicit CharField for message_body (even if ModelSerializer infers it)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    # Nested messages in the conversation using SerializerMethodField
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        # Return serialized messages related to this conversation
        messages = obj.message_set.all()  # or obj.messages if related_name set
        serializer = MessageSerializer(messages, many=True)
        return serializer.data

    def validate_participants(self, value):
        # Example validation, raise ValidationError if participants < 2
        if len(value) < 2:
            raise serializers.ValidationError("Conversation must have at least two participants.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
