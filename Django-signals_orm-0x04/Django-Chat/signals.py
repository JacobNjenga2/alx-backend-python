from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        # Check if content is being changed
        if old_message.content != instance.content:
            # Save old content to history
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True
