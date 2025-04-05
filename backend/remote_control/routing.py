from django.urls import path
from remote_control.consumers import RemoteControlConsumer

websocket_urlpatterns = [
    path("ws/remote/", RemoteControlConsumer.as_asgi()),
]
