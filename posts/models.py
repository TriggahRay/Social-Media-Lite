from django.db import models
from django.utils import timezone
from accounts.models import User 

# Create your models here.

#Just being ambitious with this one if it works great if not, still okay
# A hash tag that can be attached to posts
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.name}"

#Kani I had to make some changes on your class.
class Post(models.Model):
    """
    Represents a post created by a user.
    A post can contain text, an optional image, a visibility setting
    """
    # VISIBILITY_CHOICES controls who can see this post.
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('followers', 'Followers Only'),
        ('private', 'Private'),
    ]

    # ForeignKey links each post to exactly one user (the author).
    # on_delete=models.CASCADE means if the user is deleted, all their posts are deleted too.
    user = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    content = models.TextField() # user types in textbox to create a post
    created_at = models.DateTimeField(auto_now_add=True) # the time the post was created/submitted
    updated_at = models.DateTimeField(auto_now=True)

    # Optional image attached to the post.
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True
    )

    # Controls post visibility. Defaults to 'public' for all new posts.
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='public'
    )

    tags = models.ManyToManyField(
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




