from django.db import models
from project.models import Project
from register.models import Profile

class Team(models.Model):
    created_by=models.ForeignKey(Profile, on_delete=models.CASCADE)
    project=models.ManyToManyField(Project)
    name=models.CharField(max_length=100)
    specialization=models.CharField(max_length=300)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    team=models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', null=True)
    user=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='member_of_teams')
    description=models.TextField(null=True)
    is_leader=models.BooleanField(default=False)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} of {self.team.name}"
