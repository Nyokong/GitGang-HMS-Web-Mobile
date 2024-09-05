from django.urls import re_path
from . import channels

websocket_urlpatterns = [
    re_path('ws/sendfeedback', channels.FeedbackConsumer.as_asgi()),
]