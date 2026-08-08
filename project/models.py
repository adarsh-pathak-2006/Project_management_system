from django.db import models
from register.models import Profile

class Project(models.Model):
    created_by=models.ForeignKey(Profile, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

