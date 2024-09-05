from django.urls import path
from . import channels

websocket_urlpatterns = [
    path('ws/sendfeedback', channels.FeedbackConsumer.as_asgi()),
]