from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from .models import Message, MessageHistory
from django.db.models.signals import pre_save

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, no previous content
        return
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Content changed — log old content
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True