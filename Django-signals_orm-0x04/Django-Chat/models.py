from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageManager(models.Manager):
    def get_threaded_conversation(self, message_id):
        # Prefetch all messages and their replies in one query
        all_messages = self.select_related('sender', 'receiver').prefetch_related('replies').all()
        message_map = {msg.id: msg for msg in all_messages}
        def build_thread(msg):
            return {
                'id': msg.id,
                'sender': msg.sender.username,
                'receiver': msg.receiver.username,
                'content': msg.content,
                'timestamp': msg.timestamp,
                'edited': msg.edited,
                'replies': [build_thread(reply) for reply in msg.replies.all()]
            }
        root = message_map.get(message_id)
        return build_thread(root) if root else None

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    objects = MessageManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
