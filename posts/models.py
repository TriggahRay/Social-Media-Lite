from django.db import models
from django.utils import timezone
from accounts.models import User 

# Create your models here.
class Post(models.Model):
    body = models.TextField() # user types in textbox to create a post
    created_on = models.DateTimeField(default=timezone.now) # the time the post was created/submitted
    author = models.ForeignKey(User, on_delete=models.CASCADE) # finds a user currently logged in

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

