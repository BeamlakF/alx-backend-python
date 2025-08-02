from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
