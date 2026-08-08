from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from register.models import Profile, User
from register.serializer import RegisterSerializer, ProfileSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView

class RegisterAPI(APIView):
    def post(self, request):
        serial=RegisterSerializer(data=request.data)
        if serial.is_valid():
            username=serial.validated_data["username"]
            email=serial.validated_data["email"]
            f_name=serial.validated_data["first_name"]
            l_name=serial.validated_data["last_name"]
            password=serial.validated_data["password"]
            role=serial.validated_data["role"]

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return Response({"message":"username or email already exists"}, status=200)
            user=User.objects.create_user(username=username, email=email, first_name=f_name, last_name=l_name, role=role, password=password)
            Profile.objects.create(user=user)
            return Response({"message":"user registered successfully"}, status=201)
        else:
            return Response(serial.errors, status=400)

class MyProfileAPI(RetrieveUpdateDestroyAPIView):
    serializer_class=ProfileSerializer
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class ProfileAPI(ListAPIView):
    serializer_class=ProfileSerializer
    queryset=Profile.objects.all()

class ProfileDetailView(RetrieveAPIView):
    serializer_class=ProfileSerializer
    queryset=Profile.objects.all()
