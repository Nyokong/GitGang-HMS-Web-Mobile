from django.urls import path, include
# from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', include(router.urls)),
    path('usr/create', views.UserCreateView.as_view(), name="create-user"),
    path('usr/update', views.UserUpdateView.as_view(), name='user-update'),
    path('usr/login', views.LoginAPIView.as_view(), name="login-user"),
    path('usrs', views.UserListViewSet.as_view(), name='users'),
    path('verify-email/<uidb64>/<token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('usr/delete/<int:pk>/', views.DeleteUserView.as_view(), name='user-delete'),

    # video views
    path('vd/lst', views.VideoView.as_view(), name='video-list'), 
    path('vd/upload-old',views.UploadVideoView.as_view(), name='video-upload'),
    path('vd/up',views.UploadVideoViewTask.as_view(), name='video-task-upload'),
    path('vd/del/<int:pk>',views.DeleteVideoView.as_view(), name='video-delete'),

    # test form path
    path('test/', views.TestAPIView.as_view(), name="test-post"),
    path('email', views.TestEmailView.as_view(), name="test-email"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
