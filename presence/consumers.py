import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.db import transaction
from .models import Presence
from .hash_helpers import get_username_from_ws


LOBBY_GROUP_NAME = "lobby"


class LobbyConsumer(WebsocketConsumer):
    """
    Very naive implementation of presence for users
    """

    def connect(self):
        self.accept()
        username = get_username_from_ws(self.channel_name)
        Presence.objects.get_or_create(username=username)
        async_to_sync(self.channel_layer.group_add)(LOBBY_GROUP_NAME, self.channel_name)
        connected_users = Presence.get_presence_items()
        async_to_sync(self.channel_layer.group_send)(
            LOBBY_GROUP_NAME,
            {"type": "lobby_message", "message": {"users": connected_users}},
        )

    def receive(self, text_data):
        pass

    def disconnect(self, _code):
        username = get_username_from_ws(self.channel_name)
        Presence.objects.filter(username=username).delete()
        connected_users = Presence.get_presence_items()
        async_to_sync(self.channel_layer.group_discard)(
            LOBBY_GROUP_NAME, self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            LOBBY_GROUP_NAME,
            {"type": "lobby_message", "message": {"users": connected_users}},
        )

    def lobby_message(self, event):
        self.send(json.dumps(event["message"]))
