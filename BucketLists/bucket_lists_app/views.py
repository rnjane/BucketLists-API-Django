from django.shortcuts import render
from rest_framework import generics, views, permissions, response, status, authtoken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from bucket_lists_app import serializers, models


class UserRegister(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class UserLogin(views.APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        serializer = serializers.UserSerializer
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return response.Response({'error': 'please provide both username and password'},
                    status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return response.Response({'error': 'Invalid credentials'},
                    status=status.HTTP_404_NOT_FOUND)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return response.Response({'token': token.key},
                    status=status.HTTP_200_OK)

