from django.shortcuts import get_object_or_404
from project.models import Project
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from project.serializers import ProjectSerializer
from register.models import Profile
from project.permissions import IsProjectCreator

class ProjectAPI(ListAPIView):
    serializer_class=ProjectSerializer
    queryset=Project.objects.all()

class ProjectDetailAPI(RetrieveAPIView):
    serializer_class=ProjectSerializer
    queryset=Project.objects.all()

class MyProjectsAPI(ListCreateAPIView):
    serializer_class=ProjectSerializer
    def get_queryset(self):
        profile_data=get_object_or_404(Profile, user=self.request.user)
        return Project.objects.filter(created_by=profile_data)

    def perform_create(self, serializer):
        profile_data=get_object_or_404(Profile, user=self.request.user)
        serializer.save(created_by=profile_data)


class MyProjectIndividualAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=ProjectSerializer
    permission_classes = [IsProjectCreator]
    queryset=Project.objects.all()
