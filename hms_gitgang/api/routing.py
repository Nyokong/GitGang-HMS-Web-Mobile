from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/sendfeedback', consumer.FeedbackConsumer.as_asgi()),
]