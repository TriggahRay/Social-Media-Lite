from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    bio =  models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to = 'profile_pics',
        blank = True,
        null = True,
    )
#Demostrate
ROLE_CHOICES = [
    ('user', 'User')
    ('admin', 'Admin')
]

def __str___(self):
    return self.username