from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from register.models import Profile

User=get_user_model()


class UserGetSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'role']

class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password', 'role']


class ProfileSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields='__all__'

class ProfileGetSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=['user', 'bio']

