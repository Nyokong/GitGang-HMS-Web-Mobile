import re
from django.core.exceptions import ValidationError

from django.db import models

# importing abstract user
from django.contrib.auth.models import AbstractUser, Group, Permission

# importing signals
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

# validate email
def validate_email(email):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(email_regex, email):
        raise ValidationError('Enter a valid email address.')

# my user model
class CustomUser(AbstractUser):
    username = models.CharField(verbose_name="Username", max_length=8, unique=True)
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
    title = models.CharField(verbose_name="title", max_length=255)
    description = models.TextField(verbose_name="description", blank=True, null=True)
    cmp_video = models.FileField(verbose_name="cmp_video",upload_to='compressed_videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        def __str__(self):
            return f'{self.user} - {self.title}'
        
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, *args, **kwargs):
    # after saved in the database run a task
    print("Signal Sent - Code now running!")

class TestForm(models.Model):
    username = models.CharField(verbose_name='username', unique=True, max_length=8)
    password = models.CharField(verbose_name='password',  max_length=80)

    class Meta:
        def __str__(self):
            return self.username
        
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # attachment is optional
    attachment= models.FileField(verbose_name="attachment",upload_to='attachments/', unique=False, null=True)
    # the time it was created
    created_at = models.DateTimeField(auto_now_add=True)
    due_data = models.DateField()

    class Meta:
        def __str__(self):
            return f'{self.title} - created: {self.created_at}'

class Submitted(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions')
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Grade(models.Model):
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_grades')
    submission = models.ForeignKey(Submitted, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(verbose_name="Percentage Grade",max_digits=3, decimal_places=2)  # e.g.,'A++', 'A+', 'B-', etc.
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        def __str__(self):
            return f'Mark: {self.grade}/100'

    # get the lette grade
    def get_letter_grade(self):
        if self.grade >= 90:
            return 'A'
        elif self.grade >= 80:
            return 'B'
        elif self.grade >= 70:
            return 'C'
        elif self.grade >= 60:
            return 'D'
        else:
            return 'F'
        
