#!/usr/bin/env python3
"""Models for chats app in messaging_app."""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields."""
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # first_name, last_name, password already provided by AbstractUser

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """Conversation between users."""
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    """Message sent by a user in a conversation."""
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"

