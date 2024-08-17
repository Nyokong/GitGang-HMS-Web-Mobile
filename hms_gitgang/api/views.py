from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, permissions, status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login

from .serializers import UserSerializer, TestFormSerializer, LoginSerializer, VideoSerializer
from .models import CustomUser, TestForm, Video

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.contrib.sessions.models import Session
from django.utils import timezone

# opencv-python
import cv2
import os

# settings
from django.conf import settings

# video compression module and adaptive streaming
import ffmpeg
import m3u8

import random


# from allauth.account.utils import send_password_reset_email

# create user viewset api endpoint
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Call the send_verification_email method with the newly created user
        # if user:
        #     self.send_verification_email(user)

        return Response({
            "user": serializer.data,
            "message": "User created successfully. Please check your email to verify account."            
        }, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user, *args, **kwargs):

        # Generate a 5-digit verification code
        verification_code = random.randint(10000, 99999)

        # get user email
        email = user.email

        # sender email
        sender = settings.EMAIL_HOST_USER

        # defining subject and message
        subject = "Account Verification"
        message = f'Your verfication code is {verification_code}'

        # send the email
        send_mail(subject, message, sender, [f'{email}'], fail_silently=False)

        return Response({'Success': "Verification email sent"}, status=status.HTTP_200_OK)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # post 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Extract validated data
            user_data = serializer.validated_data
            # print(user_data)

            # Authenticate the user
            user = authenticate(username=user_data['username'], password=user_data['password'])

            print("Existing user: ",user)

            # target_key = '_auth_user_id'
            # target_value = '3'
            
            # this checks if the user exists
            if user is not None:
                # Create or get the token for the user
                # token, created = Token.objects.get_or_create(user=user)
                loggedUser = CustomUser.objects.get(username=user)
                # Log the user in
                login(request, user)

                # print(request.session.session_key)
                # Check if session exists
                # if request.user.is_authenticated:
                #     # Get all sessions
                #     sessions = Session.objects.filter(expire_date__gte=timezone.now())
                    # for session in sessions:
                    #     data = session.get_decoded()
                        # Loop through the dictionary
                        # for key, value in data.items():
                        #     if key == target_key and value == target_value:
                        #         print(f"Found: {key} = {value}")
                        #         break
                        # print(data)
                    
                
                # Send back a response with the token
                return Response({'sessionid': request.session.session_key},status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TestAPIView(generics.GenericAPIView):
    serializer_class = TestFormSerializer

    # post 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Print data to console
            print(request.data)
            # Send back a response
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class verify Email view 
class VerifyEmailView(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            uid=urlsafe_base64_decode(uidb64).decode('utf-8')
            user=CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator(user, token):
            user.is_active=True
            user.save()
            return Response({"message":"Email verified successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)
    
    
# user display viewset
class UserListViewSet(APIView):

    # gets users who are authenticated
    # for later purpose permissions might change
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        query = CustomUser.objects.all()
        serializer = UserSerializer(query, many=True)

        return Response(serializer.data)
    
class VideoView(generics.GenericAPIView):
    # a class the views all the videos
    # in the database all of them
    pass

class UploadVideoView(generics.CreateAPIView):
    serializer_class = VideoSerializer

    # only authenticated users can access this page?
    permission_classes = [IsAuthenticated]

    # post 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Print data to console
            print(request.data)
            video = serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
