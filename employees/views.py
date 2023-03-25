import json
from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework import generics
from django.contrib.auth import login, authenticate, logout, models
from rest_framework import response, status
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny
)
from rest_framework.decorators import permission_classes
from employees.models import Employee
from employees.serializers import (
    EmployeeSerializer,
    UserSerializer,
    UserRegisterSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return response.Response(
                {'msg': 'Already logged in'},
                status=status.HTTP_200_OK
            )

        user_data = UserSerializer(data=request.data)
        if user_data.is_valid(raise_exception=True):
            username = user_data.validated_data['username']
            password = user_data.validated_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return response.Response(
                {'msg': 'Logged In.'},
                status=status.HTTP_200_OK
            )
        return response.Response(
            {'msg': 'Check your username or password.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        logout(request)
        return response.Response( {'msg': 'Successfully logged out'}, status=status.HTTP_200_OK
        )


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = models.User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            'msg': 'Registered Successfully',
            'username': serializer.validated_data['username'],
        }
        return response.Response(data, status=status.HTTP_201_CREATED)
