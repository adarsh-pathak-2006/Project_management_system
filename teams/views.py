from django.shortcuts import get_object_or_404
from teams.serializers import TeamGetSerializer, TeamSerializer, MemberSerializer, MemberAddSerializer
from teams.models import Team, Member
from rest_framework.views import APIView
from rest_framework.response import Response
from register.models import Profile
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from teams.permissions import IsTeamLeaderOrReadOnly, IsTeamLeaderForMemberAction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

@method_decorator(cache_page(60 * 15), name='get')
@method_decorator(vary_on_headers("Authorization"), name='get')
class TeamAPI(APIView):
    def get(self, request):
        data=Team.objects.all()
        serial=TeamGetSerializer(data, many=True)
        return Response(serial.data, status=200)

    def post(self, request):
        serial=TeamSerializer(data=request.data)
        if serial.is_valid():
            profile_data=get_object_or_404(Profile, user=request.user)
            team_data=serial.save(created_by=profile_data)
            Member.objects.create(team=team_data, user=profile_data, is_leader=True)
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)
    

class TeamIndividualAPI(APIView):
    permission_classes = [IsTeamLeaderOrReadOnly]

    def get(self, request, pk):
        data=get_object_or_404(Team, id=pk)
        self.check_object_permissions(request, data)
        serial=TeamGetSerializer(data)
        return Response(serial.data, status=200)

    def put(self, request, pk):
        instance=get_object_or_404(Team, id=pk)
        self.check_object_permissions(request, instance)
        serial=TeamSerializer(instance, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=200)
        return Response(serial.errors, status=400)

    def delete(self, request, pk):
        instance=get_object_or_404(Team, id=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(status=204)

@method_decorator(cache_page(60 * 15), name='get')
@method_decorator(vary_on_headers("Authorization"), name='get')
class MemberAPI(ListAPIView):
    serializer_class=MemberSerializer
    queryset=Member.objects.all()

class MemberAddAPI(APIView):
    def post(self, request):
        team_id = request.data.get('team')
        if not team_id:
            return Response({"detail": "team field is required."}, status=400)
        
        team_instance = get_object_or_404(Team, id=team_id)
        
        # Manually check if user is leader
        try:
            leader_member = Member.objects.get(team=team_instance, user__user=request.user)
            if not leader_member.is_leader:
                return Response({"detail": "You do not have permission to perform this action. Only team leaders can add members."}, status=403)
        except Member.DoesNotExist:
            return Response({"detail": "You do not have permission to perform this action. Only team leaders can add members."}, status=403)

        serial=MemberAddSerializer(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=201)
        return Response(serial.errors, status=400)

class MemberIndividualAPI(RetrieveDestroyAPIView):
    serializer_class=MemberSerializer
    queryset=Member.objects.all()
    permission_classes = [IsTeamLeaderForMemberAction]
