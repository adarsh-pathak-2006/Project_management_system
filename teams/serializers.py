from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from teams.models import Team, Member
from project.serializers import ProjectSerializer
from project.models import Project
from register.serializer import ProfileGetSerializer


class TeamGetSerializer(ModelSerializer):
    project=ProjectSerializer(read_only=True, many=True)
    class Meta:
        model=Team
        fields='__all__'

class TeamSerializer(ModelSerializer):
    project=PrimaryKeyRelatedField(queryset=Project.objects.all(), many=True, required=False)
    created_by=ProfileGetSerializer(read_only=True)
    class Meta:
        model=Team
        fields='__all__'

class MemberSerializer(ModelSerializer):
    team=TeamGetSerializer(read_only=True)
    user=ProfileGetSerializer(read_only=True)
    class Meta:
        model=Member
        fields='__all__'

class MemberAddSerializer(ModelSerializer):
    team=PrimaryKeyRelatedField(queryset=Team.objects.all())
    class Meta:
        model=Member
        fields='__all__'