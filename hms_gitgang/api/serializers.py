from rest_framework import serializers

from .models import CustomUser, Video, TestForm

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# we are importing videoFileClip to compress
from moviepy.editor import VideoFileClip as vp 

# import os
import os

class UserSerializer(serializers.ModelSerializer):

    # password confirmation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')
        # passwords should not be returned upon response
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        # password = validate_password.pop('password')
        # password2 = validate_password.pop('password2')

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password field didnt match."})
        
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])

        # wait until account is verified before activating
        user.is_active=False
        user.save()

        # after all return user
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=80)

    class Meta:
        model = TestForm
        fields = ('username', 'password')


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'cmp_video']

    def create(self, validated_data):
        file = Video(
            user=self.context['request'].user,
            title=validated_data['title'],
            description=validated_data['description'],
            cmp_video=validated_data['cmp_video']
        )

        file.save()

        # after all return user
        return file
    
class VideoCompSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'cmp_video']

    def create(self, validated_data):
        vid_file = validated_data.get('cmp_video')
        vid_path = vid_file.temporary_file_path()

        # compress the video
        cl = vp(vid_path)
        comp_path = f'{os.path.splitext(vid_path)[0]}_com.mp4'
        cl.write_videofile(comp_path, codec='libx264', bitrate='500k')

        # remove the original file
        os.remove(vid_path)

        validated_data['comp_video'] = comp_path

        # assign video object
        file = Video(
            user=self.context['request'].user,
            title=validated_data['title'],
            description=validated_data['description'],
            cmp_video=validated_data['cmp_video']
        )

        # then save file object
        file.save()
        # after all return user
        return file

class TestFormSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=80)

    class Meta:
        model = TestForm
        fields = ('username', 'password')
