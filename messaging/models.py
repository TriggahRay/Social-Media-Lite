# messaging/models.py
from django.db import models
from accounts.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )

    # Add default='' to satisfy the existing rows issue
    content = models.TextField(default='')

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:40]}"