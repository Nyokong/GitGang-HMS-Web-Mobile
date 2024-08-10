import re
from django.core.exceptions import ValidationError

from django.db import models

# importing abstract user
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

# validate email
def validate_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(email_regex, email):
        raise ValidationError('Enter a valid email address.')

# my user model
class CustomUser(AbstractUser):
    username = models.CharField(verbose_name="student_id", max_length=8, unique=True)
    is_lecturer = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_perms')

    USERNAME_FIELD = 'username'
    
    # overwrite the model save function
    # this will do something before saving
    def save(self, *args, **kwargs):
        # overwrite the default email to the school email
        # this will set the default email into the default school email
        if not self.email:
            self.email = f"{self.username}@mynwu.ac.za" 

        super().save(*args, **kwargs)

    class Meta:
        def __str__(self):
            return self.username
        
class CustomGroup(models.Model):
    # Your custom group fields
    pass

# video uploading model
class Video(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # i want to only store compressed files
    # video_file = models.FileField(upload_to='videos/')
    compressed_file = models.FileField(upload_to='compressed_videos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
