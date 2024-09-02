from rest_framework import serializers

from .models import CustomUser, Video, TestForm, CreateAssignment, Assignment

from django.contrib.auth.password_validation import validate_password

from .validators import validate_file_size

# user creation serializer/form
class UserSerializer(serializers.ModelSerializer):

    # password confirmation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name' , 'email','is_lecturer', 'password', 'password2')
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

# user can only change details password change will done differently
class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name')
        

# user login serializer - only need username and password
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=80)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

# create assignment serializer - only lecturer can access this.
class AssignmentForm(serializers.Serializer):

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']

# video create serializer - only students can see this
class VideoSerializer(serializers.ModelSerializer):
    cmp_video = serializers.FileField(validators=[validate_file_size])
    
    class Meta:
        model = Video
        fields = ['title', 'description', 'cmp_video']

    def validate(self, data):
        validate_file_size(data['cmp_video'])
        return data

    def create(self, validated_data):
        
        file = Video(
            user=self.context['request'].user,
            title=validated_data['title'],
            description=validated_data['description'],
            cmp_video=validated_data['cmp_video']
        )

        # save the video if is succesful
        file.save()
        # after all return user
        return file

# video view list 
class Videoviewlist(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id','title', 'description', 'cmp_video']


# test - serializer
class TestFormSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=80)

    class Meta:
        model = TestForm
        fields = ('username', 'password')
# delete -serializer
class UserDeleteSerializer(serializers.ModelSerializer):
    def validate(self, data):

         return data
    def delete_user(self, user):
        user.delete()
# create assignment serializer

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateAssignment
        fields = ['id', 'user', 'message', 'uploaded_file', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        assignment = CreateAssignment.objects.create(user=user, **validated_data)
        return assignment