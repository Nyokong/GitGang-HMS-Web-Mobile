from django.db import models

# importing abstract user
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

# my user model
class CustomUser(AbstractUser):
    username = models.CharField(verbose_name="student_id", max_length=8, unique=True)
    is_lecturer = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_perms')

    USERNAME_FIELD = 'username'

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
