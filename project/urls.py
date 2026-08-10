from django.urls import path
from project.views import ProjectAPI, ProjectDetailAPI, MyProjectsAPI, MyProjectIndividualAPI

urlpatterns = [
    path('', ProjectAPI.as_view(), name='projects'),
    path('<int:pk>/', ProjectDetailAPI.as_view(), name='project_detail'),
    path('my-projects/', MyProjectsAPI.as_view(), name='my_projects'),
    path('my-projects/<int:pk>/', MyProjectIndividualAPI.as_view(), name='my_project_detail'),
]
