from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=[('ADMIN', 'Admin'), ('USER', 'User')]
    role=models.CharField(max_length=10, choices=ROLE_CHOICES)


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(null=True)
    profile_pic=models.ImageField(upload_to='pfp/', null=True)
    created_by=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

