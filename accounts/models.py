from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True, 
        default='profile_pics/default.png'
    )
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()

    def get_posts_count(self):
        return self.posts.count()