from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Video, TestForm, Assignment, Submitted, Grade, VerificationToken, FeedbackMessage

class CustomUserAdmin(UserAdmin): 

    exclude = ('date joined' ,'custom_user_perms', 'last login', 'custom_users', 'superuser status')

    # If you're using fieldsets:
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name' ,'email', 'password', 'is_staff', 'is_active')}),
    )

class CustomTestAdmin():
    fieldsets = (
        (None, {
            "fields": (
                'username', 'password',
            ),
        }),
    )
    

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationToken)
admin.site.register(Video)
admin.site.register(TestForm)
admin.site.register(Assignment)
admin.site.register(Submitted)
admin.site.register(Grade)
admin.site.register(FeedbackMessage)
