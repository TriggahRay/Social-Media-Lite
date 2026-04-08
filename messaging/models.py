from django.db import models
from accounts.models import User

# Create your models here.

#A message sent from one user to another.
class Message(models.Model):
     # The user who wrote and sent the message.
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
)
    
# The user who should receive and read the message.
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

content = models.TextField()
is_read = models.BooleanField(default=False)
created_at = models.DateTimeField(auto_now_add=True)

#Orders Messages by the time/day created
class Meta:
    ordering = ['created_at']

def __str__(self):
    return f"{self.sender.username} to {self.receiver.username}: {self.content[:40]}"