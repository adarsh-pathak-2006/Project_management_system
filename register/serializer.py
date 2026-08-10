from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import get_user_model
from register.models import Profile

User=get_user_model()


class UserGetSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'role', 'first_name', 'last_name']

class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {'role': {'required': False}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'USER')
        )
        return user


class ProfileSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    member_of_teams=SerializerMethodField()

    class Meta:
        model=Profile
        fields='__all__'
    
    def get_member_of_teams(self, obj):
        from teams.serializers import MemberSerializer
        # We can use MemberSerializer but that also imports team. Let's see what is needed.
        # It's better to avoid nested imports if they are heavy.
        from teams.models import Member
        members = obj.member_of_teams.all()
        # Since MemberGetSerializer in teams doesn't exist, we can just return a basic dict
        return [
            {
                "team_id": member.team.id,
                "team_name": member.team.name,
                "is_leader": member.is_leader
            } for member in members if member.team
        ]

class ProfileGetSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=['user', 'bio']
