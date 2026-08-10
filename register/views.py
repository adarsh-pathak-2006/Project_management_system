from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from register.models import Profile, User
from register.serializer import RegisterSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serial = RegisterSerializer(data=request.data)
        if serial.is_valid():
            user = serial.save()
            Profile.objects.create(user=user)
            return Response({"message": "user registered successfully"}, status=201)
        else:
            return Response(serial.errors, status=400)

class MyProfileAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class ProfileAPI(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class ProfileDetailView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
