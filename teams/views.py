from django.shortcuts import get_object_or_404
from teams.serializers import TeamGetSerializer, TeamSerializer, MemberGetSerializer, MemberSerializer
from teams.models import Team, Member
from rest_framework.views import APIView
from rest_framework.response import Response
from register.models import Profile


class TeamAPI(APIView):
    def get(self, request):
        data=Team.objects.all()
        serial=TeamGetSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request):
        serial=TeamSerializer(data=request.data)
        if serial.is_valid():
            team_data=serial.save()
            profile_data=get_object_or_404(Profile, user=request.user)
            Member.objects.create(team=team_data, user=profile_data, is_leader=True)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)
    
