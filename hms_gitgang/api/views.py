from django.shortcuts import render

from rest_framework import viewsets, permissions, generics, permissions, status
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action

from .serializers import UserSerializer
from .models import CustomUser

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

# create user viewset api endpoint
class UserCreateView(generics.CreateAPIView):
    # create a serializer
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # sending email for verification
        self.send_verification_email(user)

        return Response({
            "user": serializer.data,
            "message": "User created successfully. Please check your email to verify account."
        }, status=status.HTTP_201_CREATED)


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



