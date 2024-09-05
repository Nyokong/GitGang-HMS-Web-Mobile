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
    path('usr/verify/', views.VerificationView.as_view(), name='verify-email'),
    path('usrs', views.UserListView.as_view(), name='users'),

    # django allauth links
    path('custom/login', views.CustomLoginView.as_view(), name='custom-login'),
    path('custom/logout', views.CustomLogoutView.as_view(), name='custom-logout'),
    path('custom/signup', views.CustomSignupView.as_view(), name='custom-signup'),

    # social login
    path('auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/google/callback/', views.GoogleCallbackView.as_view(), name='google_callback'),

    # video views
    path('vd/lst', views.VideoView.as_view(), name='video-list'), 
    path('vd/upload-old',views.UploadVideoView.as_view(), name='video-upload'),
    path('vd/up',views.UploadVideoViewTask.as_view(), name='video-task-upload'),
    path('vd/del/<int:pk>',views.DeleteVideoView.as_view(), name='video-delete'),

    # assignment url enpoints
    path('asmt/create', views.AssignmentView.as_view(), name='assignment-create'), 

    # feedback http endpoints
    path('feedback/msgs', views.FeedbackMessages.as_view(), name='feedback-msgs'),

    # test form path
    path('test', views.TestAPIView.as_view(), name="test-post"),
    path('email', views.TestEmailView.as_view(), name="test-email"),
    path('tokens', views.TestTokens.as_view(), name="test-email"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
