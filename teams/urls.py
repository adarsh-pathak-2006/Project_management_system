from django.urls import path
from teams.views import TeamAPI, TeamIndividualAPI, MemberAPI, MemberAddAPI, MemberIndividualAPI

urlpatterns = [
    path('', TeamAPI.as_view(), name='teams'),
    path('<int:pk>/', TeamIndividualAPI.as_view(), name='team_detail'),
    path('members/', MemberAPI.as_view(), name='members'),
    path('members/add/', MemberAddAPI.as_view(), name='member_add'),
    path('members/<int:pk>/', MemberIndividualAPI.as_view(), name='member_detail'),
]
