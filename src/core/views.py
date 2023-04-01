import json

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serialize import UserCreateSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not (user := authenticate(
            username=request.data['username'],
            password=request.data['password']
        )):
            raise AuthenticationFailed
        login(request=request, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


