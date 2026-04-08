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
     #The user doing the following
     follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
     #The user being followed
     following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
     
created_at = models.DateTimeField(auto_now_add=True)

class Meta:
     unique_together = ('follower', 'following')

def __str__(self):
    return f"{self.follower.username} follows {self.following.username}"

#Allowed Notifications
class Notification(models.Model):
    
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('message', 'Message'),
    ]

    #The user who receives the notification.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    #Type of notification triggered
    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES
    )
    #Description of the notification
    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    #link to the post triggered the like
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    ) 

    #Time of the Notification
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         ordering = ['-created_at']

def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
   
