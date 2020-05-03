from django.db import models
import json
from .board_utils import (
    generate_board,
    parse_board_from_string,
    board_full,
    find_winner,
)
from .move_utils import translate_move, next_turn


# Create your models here.
class Game(models.Model):
    """
    Stores the game state.
    Avoid using save() after modifying the board in another layer to keep integrity.
    Use the add_move method instead to add new player movements.
    """

    player_1 = models.CharField(max_length=30, default="")
    player_2 = models.CharField(max_length=30, default="")
    board = models.TextField(default=generate_board)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    winner = models.BooleanField(null=True, default=None)

    def __str__(self):
        return "{} vs {}".format(self.player_1, self.player_2)

    def to_json(self):
        return json.dumps(
            {
                "board": self.python_board,
                "player_1": self.player_1,
                "player_2": self.player_2,
                "started": self.started,
                "finished": self.finished,
                "winner": self.winner,
                "next_player": self.get_next_player_turn(),
                "moves": [x.to_dict() for x in Move.objects.filter(game=self)],
            }
        )

    def get_next_player_turn(self):
        """
        Checks the board to find who is next
        """
        return next_turn(self.python_board)

    @property
    def python_board(self):
        return parse_board_from_string(self.board)

    def check_finished(self):
        return board_full(self.python_board)

    def add_move(self, player, new_move):
        """
        Check that the move is valid, and if it is, persist it to the database
        """
        trans_move = translate_move(self.python_board, player, new_move)
        if trans_move is not None and not self.finished:
            board = self.python_board
            board[trans_move] = player
            winner = find_winner(board, trans_move)
            if winner is None:
                self.finished = self.check_finished()
            else:
                self.winner = winner
                self.finished = True
            self.board = generate_board(board)

            # Save move and board
            player_name = self.player_1 if player else self.player_2
            Move.objects.create(game=self, move=new_move, player_name=player_name)
            self.save()
        return self


class Move(models.Model):
    """
    This class stores the moves for the game.
    This will be useful to display a list of moves to the users.
    """

    game = models.ForeignKey(Game, null=False, on_delete=models.CASCADE)
    move = models.CharField(max_length=5)
    player_name = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def to_dict(self):
        return {
            "player_name": self.player_name,
            "move": self.move,
            "timestamp": self.timestamp.isoformat(),
            "id": self.id,
        }
