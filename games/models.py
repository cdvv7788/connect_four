from django.db import models
from django.db.models import Q
import json
from .board_utils import (
    pickle_board,
    generate_board,
    parse_board_from_string,
    board_full,
    find_winner,
)
from .move_utils import translate_move, next_turn

BOARD_SIZE = 7
GAME_STATUS = [
    ("PENDING", "Pending"),
    ("STARTED", "Started"),
    ("FINISHED", "Finished"),
]


class GameManager(models.Manager):
    def create(self, **kwargs):
        """
        Override the method to generate a board with the BOARD_SIZE
        Lambdas and closures don't play well with django migrations
        """
        kwargs["board"] = generate_board(BOARD_SIZE)
        return super().create(**kwargs)

    def make_seat(self, player_name):
        """
        Looks for empty seats to occupy. Create a new game if
        no suitable game is found.
        """
        empty_games = self.filter(~Q(status="FINISHED")).filter(player_2="")
        game = None
        if empty_games.exists():
            game = empty_games.first()
            game.player_2 = player_name
            game.status = "STARTED"
            game.save()
        else:
            game = self.create(player_1=player_name)

        return game

    def find_game(self, player_name):
        """
        Finds a game for the player and joins it
        """
        unfinished_games = self.filter(~Q(status="FINISHED"))
        current_games = unfinished_games.filter(
            Q(player_1=player_name) | Q(player_2=player_name)
        )
        if current_games.exists():
            current_game = current_games.first()
        else:
            current_game = self.make_seat(player_name)
        return current_game


# Create your models here.
class Game(models.Model):
    """
    Stores the game state.
    Avoid using save() after modifying the board in another layer to keep integrity.
    Use the change_state_forward method instead to add new player movements.
    """

    player_1 = models.CharField(max_length=30, default="")
    player_2 = models.CharField(max_length=30, default="")
    board = models.TextField(default="")
    status = models.CharField(
        default=GAME_STATUS[0][0], max_length=8, choices=GAME_STATUS
    )
    winner = models.BooleanField(null=True, default=None)
    objects = GameManager()

    def __str__(self):
        return "{} vs {}".format(self.player_1, self.player_2)

    def to_json(self):
        return json.dumps(
            {
                "board": self.python_board,
                "player_1": self.player_1,
                "player_2": self.player_2,
                "status": self.status,
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

    @property
    def finished(self):
        return self.status == "FINISHED"

    @property
    def started(self):
        return self.status == "STARTED"

    def check_finished(self):
        return board_full(self.python_board)

    def change_state_forward(self, player, new_move):
        """
        Check that the move is valid, and if it is, persist it to the database
        All the side-effects are contained in this method, so additional changes are performed too
        """
        trans_move = translate_move(self.python_board, player, new_move)
        if trans_move is not None and not self.finished:
            board = self.python_board
            board[trans_move] = player
            winner = find_winner(board, trans_move)
            self.board = pickle_board(board)
            if winner is None:
                self.status = "FINISHED" if self.check_finished() else self.status
            else:
                self.winner = winner
                self.status = "FINISHED"

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
