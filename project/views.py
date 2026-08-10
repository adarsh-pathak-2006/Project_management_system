from django.shortcuts import get_object_or_404
from project.models import Project
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from project.serializers import ProjectSerializer
from register.models import Profile
from project.permissions import IsProjectCreator

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

class ProjectAPI(ListAPIView):
    serializer_class=ProjectSerializer
    queryset=Project.objects.all()

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers("Authorization"))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
