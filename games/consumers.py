import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.db import transaction
from .models import Game, Move


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game = Game.objects.get(id=self.game_id)

        async_to_sync(self.channel_layer.group_add)(self.game_id, self.channel_name)

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.game_id, {"type": "game_message", "message": self.game.to_json()}
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.game_id, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if "replay_until" in text_data_json.keys():
            last_move_id = text_data_json["replay_until"]
            last_move = Move.objects.get(id=last_move_id)
            board = last_move.reconstruct_up_to()
            self.send(json.dumps({"replay_board": board}))

        else:
            move = text_data_json["move"]
            move[0] = int(move[0])
            player = text_data_json["player"] == self.game.player_1
            game = Game.objects.select_for_update().get(id=self.game.id)
            with transaction.atomic():
                self.game = game.change_state_forward(player, move)

            async_to_sync(self.channel_layer.group_send)(
                self.game_id, {"type": "game_message", "message": self.game.to_json()}
            )

    def game_message(self, event):
        self.send(event["message"])
