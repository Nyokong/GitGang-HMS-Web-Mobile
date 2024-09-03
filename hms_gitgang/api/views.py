from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, permissions, status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
import requests

# auth
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login

# Oauth2
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView
from oauth2_provider.views import application

from .serializers import UserSerializer, UserUpdateSerializer,TestFormSerializer, Videoviewlist,LoginSerializer, VideoSerializer
from .models import CustomUser, TestForm, Video, VerificationToken

# from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.contrib.sessions.models import Session
from django.utils import timezone

# opencv-python

import os
import random

# settings
from django.conf import settings

# video compression module and adaptive streaming
import m3u8

import moviepy.editor as mp


# from allauth.account.utils import send_password_reset_email

# create user viewset api endpoint
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})

        # is not valid = "this data does not match"
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Call the send_verification_email method with the newly created user
        if user:
            self.send_verification_email(user)

        return Response({
            "user": serializer.data,
            "message": "User created successfully. Please check your email to verify account."            
        }, status=status.HTTP_201_CREATED)

    def send_verification_email(self, user, *args, **kwargs):

        # Generate a 5-digit verification code
        verification_code = random.randint(10000, 99999)

        key = get_random_string(length=32)
        
        VerificationToken.objects.create(user=user, token=key)

        verification_link = f'http://127.0.0.1:8000/api/usr/verify/?key={key}'

        # get user email
        email = user.email

        # sender email
        sender = settings.EMAIL_HOST_USER

        # defining subject and message
        subject = "Non-reply | Account Verification"
        message = f'Hey-ya \nYour verfication code is {verification_code} \n\n Click this link to verify account: {verification_link}\n non-reply email'

        # send the email
        send_mail(subject, message, sender, [f'{email}'], fail_silently=False)

        return Response({'Success': "Verification email sent"}, status=status.HTTP_200_OK)

class VerificationView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()

    permission_classes = [permissions.AllowAny]

    def get_object(self):
        # Get the user instance based on the verification token
        # get token on the verification url
        token = self.request.query_params.get('token')

        try:
            user = VerificationToken.objects.get(token=token)
        except VerificationToken.DoesNotExist:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)

        # return user
        return user

    def get(self, request):
        # token = request.query_params.get('token')
        token_user = self.get_object()

        # get user from custom user and acivate user
        try:
            user = CustomUser.objects.get(username=token_user.user)

            user.is_active = True
            user.save()
       
            return Response({'message': 'User activated successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User DoesntExisist'}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.RetrieveUpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer 

    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data,instance=user)

        # if user is valid - check 
        if serializer.is_valid():
            user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

# this is the Login View
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

            print("Existing user: ",user) # error handling 

            # target_key = '_auth_user_id'
            # target_value = '3'
            
            # this checks if the user exists
            if user is not None:
                # Create or get the token for the user
                # token, created = Token.objects.get_or_create(user=user)
                loggedUser = CustomUser.objects.get(username=user)

                # Log the user in
                login(request, user)

                # create a session        

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
    
from allauth.account import views as account_views

class CustomLoginView(account_views.LoginView):

    def get_success_url(self):
        # Perform custom actions after login
        # ...

        return super().get_success_url()
    
class CustomLogoutView(account_views.LogoutView):
    
    def get_success_url(self):
        # Perform custom actions after login
        # ...

        return super().get_success_url()
    
class CustomSignupView(account_views.SignupView):
    
    def get_success_url(self):
        # Perform custom actions after login
        # ...

        return super().get_success_url()

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class GoogleCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'No code provided'}, status=400)

        # Exchange code for tokens
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'redirect_uri': '/',
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=data)
        tokens = response.json()

        access_token = tokens.get('access_token')
        id_token = tokens.get('id_token')

        # Verify ID token and get user info
        user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        return Response(user_info)

# user display viewset
class UserListViewSet(APIView):

    # gets users who are authenticated
    # for later purpose permissions might change
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        query = CustomUser.objects.all()
        serializer = UserSerializer(query, many=True)

        return Response(serializer.data)
    
class VideoView(generics.GenericAPIView):
    # a class the views all the videos
    # in the database all of them
    permission_classes = [permissions.AllowAny]
    serializer_class = Videoviewlist

    # overwrite the get query method
    def get_queryset(self):
        return Video.objects.all()

    def get(self, request, format=None):
        query = self.get_queryset()

        serializer = self.get_serializer(query, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteVideoView(generics.DestroyAPIView):
    # a class the views all the videos
    # in the database all of them
    permission_classes = [permissions.AllowAny]

    # retrieve all videos
    def get_queryset(self):
        return Video.objects.all()  

class UploadVideoView(generics.CreateAPIView):
    serializer_class = VideoSerializer  

    # only authenticated users can access this page?
    permission_classes = [IsAuthenticated]

    # post 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Print data to console
            print('video upload in progress') # error handling 
            video = serializer.save()
            print('Original Video Uploaded!')
            # my_task("yes my task")
            
            # Process the video for adaptive streaming
            file_obj = request.data['cmp_video']
            input_file_path = file_obj.temporary_file_path()

            # Debugging: Check if the file exists
            if not os.path.exists(input_file_path):
                return Response({"error": "Temporary file not found"}, status=status.HTTP_400_BAD_REQUEST)


            # Start background task
            # Create the subfolder inside 'hls_videos'
            subfolder_path = os.path.join(settings.MEDIA_ROOT, 'hls_videos', str(video.id))

            output_dir = os.path.join(settings.MEDIA_ROOT, 'hls_videos', str(video.id))

            os.makedirs(output_dir, exist_ok=True)

            # Set the temp directory for moviepy
            temp_dir = os.path.join(subfolder_path, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            os.environ['TEMP'] = temp_dir
            os.environ['TMPDIR'] = temp_dir

            try:
                # Load the video file
                video = mp.VideoFileClip(input_file_path).resize(0.5)

                # Split the video into segments (e.g., 10 seconds each)
                segment_duration = 5
                segments = []

                print("now cutting into segments")
                for i in range(0, int(video.duration), segment_duration):
                    # create the segments
                    segment = video.subclip(i, min(i + segment_duration, video.duration))

                    # Ensure audio is included and specify temp audio file location
                    temp_audiofile = os.path.join(temp_dir, f'temp_audio_{i}.m4a')

                    # create segment path
                    segment_file = os.path.join(subfolder_path, str(f'segment_{i}.ts'))
                    
                    segment.write_videofile(segment_file, codec='libx264',audio_codec='aac', temp_audiofile=temp_audiofile)

                    segments.append(segment_file)

                # Create the M3U8 playlist
                playlist = m3u8.M3U8()
                for segment_file in segments:
                    playlist.add_segment(m3u8.Segment(uri=segment_file, duration=segment_duration))

                # Save the playlist to a file in the subfolder
                playlist_file = os.path.join(subfolder_path, 'playlist.m3u8')
                with open(playlist_file, 'w') as f:
                    f.write(playlist.dumps())

                # Clean up temporary files
                for temp_file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, temp_file))

                return Response({"message": "HLS playlist created successfully!", "playlist": playlist_file}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error during HLS creation: {e}")
                return Response({"error": "HLS creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadVideoViewTask(generics.CreateAPIView):
    serializer_class = VideoSerializer  

    # only authenticated users can access this page?
    permission_classes = [IsAuthenticated]

    # post 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Print data to console
            print('video upload in progress')
            video = serializer.save()
            print('Original Video Uploaded!')

            # return the success response
            return Response({"view": "view is a success!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# tests
class TestEmailView(generics.GenericAPIView):
    serializer_class = None

    def get(self, request):
        # Send the email
        # send_mail(
        #     'Test Email',
        #     'This is a test email from Django.',
        #     'callmekaywork@gmail.com',
        #     ['mikewolfnyokong@gmail.com'],
        #     fail_silently=False,
        # )
        verification_code = random.randint(10000, 99999)
        subject = "Account Verification"
        message = f'Your verfication code is {verification_code}'
        sender = settings.EMAIL_HOST_USER
        email = ['mikewolfnyokong@gmail.com']
        
        send_mail(subject, message, sender, email, fail_silently=False)

        # Return a success message
        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)

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

class TestTokens(APIView):
    serializer_class = None
    permission_classes = [permissions.AllowAny]

    def get_object(self, request, format=None):
        # Get the user instance based on the verification token
        # get token on the verification url
        token = self.request.query_params.get('token')
        print("Token From Url: ", token)

        try:
            user = VerificationToken.objects.get(token=token)
        except VerificationToken.DoesNotExist:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)

        # return user
        return user

    def get(self, request, format=None):
        user = self.get_object()

        return Response({f'logged in user: {user}'}, status=status.HTTP_200_OK)
    