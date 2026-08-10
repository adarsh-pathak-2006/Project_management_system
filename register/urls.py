from django.urls import path
from register.views import RegisterAPI, MyProfileAPI, ProfileAPI, ProfileDetailView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('profile/me/', MyProfileAPI.as_view(), name='my_profile'),
    path('profile/', ProfileAPI.as_view(), name='profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
]
