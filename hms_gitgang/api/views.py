from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, permissions
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action

from .serializers import UserSerializer
from .models import CustomUser


# create user viewset api endpoint
class UserCreateViewSet(generics.CreateAPIView):
    # retrieve all users
    query = CustomUser.objects.all()

    serializer_class = UserSerializer

    # temp
    # allow any user to create an account
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=['post'])
    # create user function
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # perfom create user
        user = self.perform_create(serializer)
        # get or create token
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
    
    
# user display viewset
class UserListViewSet(APIView):

    # gets users who are authenticated
    # for later purpose permissions might change
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        query = CustomUser.objects.all()
        serializer = UserSerializer(query, many=True)

        return Response(serializer.data)



