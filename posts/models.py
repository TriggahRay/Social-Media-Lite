from django.db import models
from django.utils import timezone
from accounts.models import User 

# Create your models here.

#Just being ambitious with this on if it works great if not, still okay
# A hash tag that can be attched to posts
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.name}"

class Post(models.Model):
    body = models.TextField() # user types in textbox to create a post
    created_on = models.DateTimeField(default=timezone.now) # the time the post was created/submitted
    author = models.ForeignKey(User, on_delete=models.CASCADE) # finds a user currently logged in

#Kani Uncomment below by removing (''') after modifying the post
'''  tags = models.ManyToManyField(
        Tag,
        through='PostTag',
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.count()


class PostTag(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_tags'
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='post_tags'
    )

    class Meta:
        unique_together = ('post', 'tag')

    def __str__(self):
        return f"{self.post} — #{self.tag.name}"
'''



