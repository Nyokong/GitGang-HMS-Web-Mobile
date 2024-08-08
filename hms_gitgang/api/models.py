from django.db import models

# importing abstract user
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

# my user model
class User(AbstractBaseUser):
    username = models.CharField(verbose_name="student_id", max_length=8)
    is_lecturer = models.BooleanField(default=False)

    class Meta:

        def __str__(self):
            return self.username
        
