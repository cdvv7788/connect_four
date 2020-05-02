from django.db import models
from operator import add
import json
import copy


def generate_blank_board():
    """
    Generates a blank board.
    None means that the position is empty
    True means player_1 picked that position
    False means player_2 picked that position
    """
    return str([None] * 7 * 7)


def parse_board_from_string(board):
    """
    Parses the board back to python
    eval is a dirty way to do this, but the window it opens for
    arbitrary code execution is troublesome. The board can be parsed
    with more strict validation and parsing rules or it can be stored in a more
    suitable format (like postgres arrays).
    For the sake of this exercise, I will use this method.
    """
    return eval(board)


def board_full(board):
    """
    Checks that all of the positions are filled
    board: python_parsed board (7x7 list)
    """
    if None in board:
        return False
    return True


def next_turn(board):
    """
    Checks the board to find who is next
    """
    counts = (board.count(True), board.count(False))
    return counts[0] == counts[1]


def translate_move(board, player, move):
    """
    Checks the following conditions:
     - It is the player's turn
     - The position is empty
     board: python representation of the board
     player: boolean representing player (True=player_1, False=player_2)
     move: tuple containing the next move. It contains the row and the side to which stack (L or R)
    """
    # If the number of plays on both sides is the same,
    # it is player_1 turn, otherwise it is player_2's turn
    if next_turn(board) == player:
        offset = move[0] * 7
        direction = (
            range(offset, offset + 7)
            if move[1] == "L"
            else range(offset + 6, offset - 1, -1)
        )
        for i in direction:
            if board[i] == None:
                return i


def apply_move(board, player, move):
    """
    This is similar to Game's add move, but it does not validate any conditions based on the state.
    It simply applies the moves to the given board for the given player, if the movement is possible.
    If the movement is not possible, the TypeError that is raised is intentionally left there.
    """
    board = copy.copy(board)
    trans_move = translate_move(board, player, move)
    board[trans_move] = player
    return board


def get_next_position(position, direction):
    """
    Given a position, find the next position in the given direction
    """
    pos_2d = (position % 7, position // 7)
    next_2d = list(map(add, pos_2d, direction))
    if next_2d[0] > 6 or next_2d[0] < 0 or next_2d[1] > 6 or next_2d[1] < 0:
        return None
    else:
        return next_2d[1] * 7 + next_2d[0]


def scan(board, direction, position, player, count=0):
    """
    Scans the board in the given position until a None, an edge or a different player piece is found
    direction: 2d array that indicates the direction to scan. I.E. (1,1) is top right diagonal
    """
    next_position = get_next_position(position, direction)
    if next_position is not None:
        if board[next_position] == player:
            count = scan(board, direction, next_position, player, count)
            count += 1
    return count


def find_winner(board, last_play):
    """
    Scans the board for winner combinations for player responsible for
    the last play
    Returns True, False or None (player_1, player_2, no winner)
    """
    player = board[last_play]
    left = scan(board, (-1, 0), last_play, player)
    right = scan(board, (1, 0), last_play, player)
    top = scan(board, (0, -1), last_play, player)
    bottom = scan(board, (0, 1), last_play, player)
    top_left = scan(board, (-1, -1), last_play, player)
    top_right = scan(board, (1, -1), last_play, player)
    bottom_left = scan(board, (-1, 1), last_play, player)
    bottom_right = scan(board, (1, 1), last_play, player)
    if (
        left + right >= 3
        or top + bottom >= 3
        or top_left + bottom_right >= 3
        or top_right + bottom_left >= 3
    ):
        return player
    else:
        return None


# Create your models here.
class Game(models.Model):
    """
    Stores the game state.
    Avoid using save() after modifying the board in another layer to keep integrity.
    Use the add_move method instead to add new player movements.
    """

    player_1 = models.CharField(max_length=30, default="")
    player_2 = models.CharField(max_length=30, default="")
    board = models.TextField(default=generate_blank_board)
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

    def _print_board(self):
        """
        Internal method to debug board state
        Prints the current board to stdout
        """
        output = ""
        board = self.python_board
        for i in range(len(board)):
            if i % 7 == 0:
                output += "\n"
            output += f" {board[i]} "
        print(output)

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
            self.board = str(board)

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
