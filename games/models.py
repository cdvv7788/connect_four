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


def translate_move(board, player, move):
    """
    Checks the following conditions:
     - It is the player's turn
     - The position is empty
     board: python representation of the board
     player: boolean representing player (True=player_1, False=player_2)
     move: tuple containing the next move. It contains the row and the side to which stack (L or R)
    """
    counts = (board.count(True), board.count(False))
    # If the number of plays on both sides is the same,
    # it is player_1 turn, otherwise it is player_2's turn
    if (counts[0] == counts[1]) == player:
        offset = move[0] * 7
        direction = (
            range(offset, offset + 7)
            if move[1] == "L"
            else range(offset + 6, offset - 1, -1)
        )
        for i in direction:
            if board[i] == None:
                return i


# Create your models here.
class Game(models.Model):
    """
    Stores the game state.
    Avoid using save() after modifying the board in another layer to keep integrity.
    Use the add_move method instead to add new player movements.
    """

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
        if trans_move is not None:
            board = self.python_board
            board[trans_move] = player
            self.board = str(board)
            self.save()
