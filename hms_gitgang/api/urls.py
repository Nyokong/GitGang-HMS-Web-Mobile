from django.urls import path, include
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()

# register the users url
# router.register(r'users', views.UserCreateViewSet, basename='users')
# router.register(r'view-users', views.UserListViewSet, basename='view-users')

urlpatterns = [
    # path('', include(router.urls)),
    path('user/create/', views.UserCreateView.as_view(), name="create-user"),
    path('users/', views.UserListViewSet.as_view(), name='users'),
    path('verify-email/<uidb64>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    # path('password/reset', views.PasswordReset.as_view(), name='password-reset'),
]
