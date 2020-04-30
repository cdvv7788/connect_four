from django.db import models


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


# Create your models here.
class Game(models.Model):
    player_1 = models.CharField(max_length=30)
    player_2 = models.CharField(max_length=30)
    board = models.TextField(default=generate_blank_board)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return "{} vs {}".format(self.player_1, self.player_2)

    @property
    def python_board(self):
        return parse_board_from_string(self.board)

    def check_finished(self):
        # TODO: Check if there is a winner
        if board_full(self.python_board):
            return True
        return False
