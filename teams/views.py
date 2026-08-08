from django.shortcuts import get_object_or_404
from teams.serializers import TeamGetSerializer, TeamSerializer, MemberSerializer
from teams.models import Team, Member
from rest_framework.views import APIView
from rest_framework.response import Response
from register.models import Profile
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView


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
    

class TeamIndividualAPI(APIView):
    def get(self, request, pk):
        data=Team.objects.all()
        serial=TeamGetSerializer(data)
        return Response(serial.data, status=200)

    def put(self, request, pk):
        instance=get_object_or_404(Team, id=pk)
        serial=TeamSerializer(instance, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.data, status=400)

    def delete(self, request, pk):
        instance=get_object_or_404(Team, id=pk)
        instance.delete
        return Response(status=204)

class MemberAPI(ListAPIView):
    serializer_class=MemberSerializer
    queryset=Member.objects.all()

class MemberIndividualAPI(RetrieveDestroyAPIView):
    serializer_class=MemberSerializer
    queryset=Member.objects.all()
    
