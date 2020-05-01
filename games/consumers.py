import json
from channels.generic.websocket import WebsocketConsumer
from .models import Game


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game = Game.objects.get(id=self.game_id)
        self.accept()
        self.send(self.game.to_json())

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
