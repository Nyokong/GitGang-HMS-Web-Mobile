from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin): 

    exclude = ('date joined' ,'custom_user_perms', 'last login', 'custom_users', 'superuser status')

    # If you're using fieldsets:
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name' ,'email', 'password', 'is_staff')}),
    )

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
