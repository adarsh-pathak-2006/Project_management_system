from rest_framework.permissions import BasePermission, SAFE_METHODS
from teams.models import Member

class IsTeamLeaderOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj is a Team instance
        try:
            member = Member.objects.get(team=obj, user__user=request.user)
            return member.is_leader
        except Member.DoesNotExist:
            return False

class IsTeamLeaderForMemberAction(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is a Member instance
        try:
            leader = Member.objects.get(team=obj.team, user__user=request.user)
            return leader.is_leader
        except Member.DoesNotExist:
            return False
