from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Post(models.Model):
    body = models.TextField() # user types in textbox to create a post
    created_on = models.DateTimeField(default=timezone.now) # the time the post was created/submitted
    author = models.ForeignKey(AbstractUser, on_delete=models.CASCADE) # finds a user currently logged in
