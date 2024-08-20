from django.urls import path, include
# from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', include(router.urls)),
    path('user/create/', views.UserCreateView.as_view(), name="create-user"),
    path('user/login/', views.LoginAPIView.as_view(), name="login-user"),
    path('users/', views.UserListViewSet.as_view(), name='users'),
    path('verify-email/<uidb64>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'),

    # video views
    path('view/videos/', views.VideoView.as_view()), 
    path('video/upload/',views.UploadVideoView.as_view(), name='video-upload'),
    # path('password/reset', views.PasswordReset.as_view(), name='password-reset'),

    # test form path
    path('test/', views.TestAPIView.as_view(), name="test-post"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
