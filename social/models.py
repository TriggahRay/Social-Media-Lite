from django.db import models 
from accounts.models import User 
from posts.models import Post

# Create your models here.


# A comment left by a user on a post.
class Comment(models.Model):

    #Which post this comment belongs to
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # Which user wrote this comment.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )


    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_at']


    def __str__(self):
        return f"{self.user.username} on Post {self.post.id}: {self.content[:40]}"

#A User liking a post
class Like(models.Model):
    #The user who gave a like
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    #The post that recieved a like
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    #Time of a like
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')

def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

#Following users
class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )
    # This MUST exist
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    # This MUST exist — the person who triggered the notification
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True, blank=True
    )
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='notifications'
    )
    # This MUST exist
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
   
