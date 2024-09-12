from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, permissions, status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate, login

from .serializers import UserSerializer, UserUpdateSerializer,TestFormSerializer, Videoviewlist,LoginSerializer, VideoSerializer, UserDeleteSerializer, AssignmentSerializer, AssignmentForm
from .models import CustomUser, TestForm, Video, Assignment

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import get_object_or_404

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

# DELETE VIEW USER
class DeleteUserView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDeleteSerializer
    permission_class = (IsAuthenticated,)

    def get_object(self):
        user_id = self.kwargs.get("pk")
        return get_object_or_404(CustomUser, id=user_id)
    
    def destroy(self, request, *args, **kwargs):
        user =self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

# assignments views
# create assignments
# class CreateAssignmentView(generics.CreateAPIView):
#     serializer_class = AssignmentSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Print data to console
#             print('serializer is valid')
#             asignment = serializer.save()

#             # return the success response
#             return Response({"view": "view is a success!"}, status=status.HTTP_201_CREATED)
        
#         return Response({'msg':'assignment created'}, status=status.HTTP_200_OK)

class AssignmentView(generics.CreateAPIView):
    serializer_class =AssignmentForm
    permission_class = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)

        if serializer.is_valid():
            #print data to console
            print('assignment upload in progress')
            serializer.save()
            #return the success response
            return Response ({"msg": "assignment creation is a success!"}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
  #display assignments created
#class AssignmentListView(generics.ListCreateAPIView):
    #queryset = Assignment.objects.all()
    #serializer_class =AssignmentForm

class AssignmentListView(generics.GenericAPIView):
        permission_classes = [permissions.AllowAny]

        def get_queryset(self):
         return Assignment.objects.all() 

        def get(self, request, format=None):
         queryset = self.get_queryset() 
         serializer = AssignmentForm(queryset, many=True)
         return Response(serializer.data)
   
    

# update assignments - only logged the lecturer
class AssignmentUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes =[permissions.AllowAny]
    queryset= Assignment.objects.all()
    serializer_class = AssignmentForm
    lookup_field ='id'

    def update(self, request, *args, **kwargs):
        try:
              # Retrieve the object
            instance = self.get_object()
            # Serialize the data with partial updates enabled
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # Save the updated instance
            self.perform_update(serializer)
            response = super().update(request, *args, **kwargs)
            return Response({
                "message": "Assignment updated succesfully",
                "data": response.data
            }, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            
            return Response({

              "message": "Assignment updated succesfully",
            "errors": e.detail
            }, status=status.HTTP_200_OK)
        except Exception as e:
           
            return Response({
                "message": "An error occurred while updating the assignment",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# delete assignments - only lecturer and admin can access

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
