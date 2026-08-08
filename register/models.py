from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=[('LEADER', 'Leader'), ('MEMBER', 'Member')]
    role=models.CharField(max_length=10, choices=ROLE_CHOICES)


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    nickname=models.CharField(max_length=50)
    bio=models.TextField(null=True)
    profile_pic=models.ImageField(upload_to='pfp', null=True)

    def __str__(self):
        return self.user.username
    

