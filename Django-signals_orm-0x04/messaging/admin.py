from django.contrib import admin
from .models import Message, Notification
from .models import MessageHistory
from .models import Reaction



admin.site.register(MessageHistory)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Reaction)

