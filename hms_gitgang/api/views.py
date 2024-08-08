from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .models import CustomUser


# create user viewset api endpoint
class UserViewSet(viewsets.ModelViewSet):

    # retrieve all users
    q = CustomUser.objects.all()

    serializer_class = UserSerializer

    # temp
    # allow any user to create an account
    permission_classes = (permissions.AllowAny,)

    # create user function
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create_(user=user)

        data = serializer.data
        data['token'] = token.key

        return Response(data, status=status.HTTP_201_CREATED)
    
    # perform create user
    def perform_create(self, serializer):

        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        return user

