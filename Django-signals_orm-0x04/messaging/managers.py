from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """Get unread messages for a specific user with optimized query."""
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id',
            'sender__username',
            'content',
            'timestamp',
            'read'
        )
