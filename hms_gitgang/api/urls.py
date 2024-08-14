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
    path('user/login/', views.LoginAPIView.as_view(), name="login-user"),
    path('users/', views.UserListViewSet.as_view(), name='users'),
    path('verify-email/<uidb64>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'),

    # video views
    path('view/videos', views.VideoView.as_view()), 
    path('video/upload',views.UploadVideoView.as_view(), name='video-upload'),
    # path('password/reset', views.PasswordReset.as_view(), name='password-reset'),

    # test form path
    path('test/', views.TestAPIView.as_view(), name="test-post"),
]
