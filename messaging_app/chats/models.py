#!/usr/bin/env python3
"""Models for messaging app: CustomUser, Conversation, and Message."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. Extend Django's User model
class CustomUser(AbstractUser):
    """Custom user model. Extend with extra fields if needed (e.g., bio, profile_pic)."""
    # Add custom fields here if you want
    # bio = models.TextField(blank=True, null=True)
    pass

# 2. Conversation Model (Many users per conversation)
class Conversation(models.Model):
    """Represents a conversation between multiple users."""
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.pk} ({self.participants.count()} participants)"

# 3. Message Model
class Message(models.Model):
    """A message sent in a conversation."""
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"

