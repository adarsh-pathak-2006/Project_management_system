from rest_framework.serializers import ModelSerializer
from project.models import Project
from register.serializer import ProfileGetSerializer

class ProjectSerializer(ModelSerializer):
    created_by=ProfileGetSerializer(read_only=True)
    class Meta:
        model=Project
        fields='__all__'
