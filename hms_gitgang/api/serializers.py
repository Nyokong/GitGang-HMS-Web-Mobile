from rest_framework import serializers

from .models import CustomUser

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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

        # sending email verification link
        self.send_verification_email(user)
        
        # after all return user
        return user

    def send_verification_email(self, user):
         # Accessing request from context
        request = self.context.get('request')
        # if not request:
        #     raise ValueError("Request context is not available in the serializer")

        token=default_token_generator.make_token(user)
        
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        verification_url=request.request.build_absolute_uri(
            reverse('verify-email', kwargs={'uidb64':uid, 'token':token})
        )

        message=f'Please click the link below to verify your email:\n{verification_url}'
        send_mail(
            'Verify Your Email',
            message,
            'callmekaywork@gmail.com',
            [user.email],
            fail_silently=False,
        )