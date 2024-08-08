from django.urls import path, include
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()

# register the users url
# router.register(r'users', views.UserCreateViewSet, basename='users')
# router.register(r'view-users', views.UserListViewSet, basename='view-users')

urlpatterns = [
    # path('', include(router.urls)),
    path('users/create/', views.UserCreateViewSet.as_view()),
    path('users/view/', views.UserListViewSet.as_view()),
]
