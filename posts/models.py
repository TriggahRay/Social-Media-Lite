from django.db import models
from django.utils import timezone
from accounts.models import User 

# Create your models here.
class Post(models.Model):
    body = models.TextField() # user types in textbox to create a post
    created_on = models.DateTimeField(default=timezone.now) # the time the post was created/submitted
    author = models.ForeignKey(User, on_delete=models.CASCADE) # finds a user currently logged in

