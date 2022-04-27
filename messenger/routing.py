from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/messenger/", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/profile/", consumers.ProfileConsumer.as_asgi())
]