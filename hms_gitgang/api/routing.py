from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/some_path/', consumer.YourConsumer.as_asgi()),
]