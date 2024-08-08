from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('usename', 'email', 'password')
        # passwords should not be returned upon response
        write_only_fields = ('password',)