from operator import add
import pickle
import base64


def generate_board(size):
    """
    Generates a blank board if no argument is passed.
    None means that the position is empty
    True means player_1 picked that position
    False means player_2 picked that position
    """
    return pickle_board([None] * size * size)


def pickle_board(board):
    """
    Pickles the passed board
    Returns a base64 representation to be able to store it in the db (utf-8 encoding).
    """
    output = pickle.dumps(board)
    return base64.b64encode(output).decode("utf-8")


def parse_board_from_string(board):
    """
    Parses the board back to python
    pickle is a dirty way to do this, as the window it opens for
    arbitrary code execution is troublesome. The board can be parsed
    with more strict validation and parsing rules or it can be stored in a more
    suitable format (like postgres arrays)
    For now, using pickle as it is slightly better than directly using eval
    For the sake of this exercise, I will use this method.
    """
    board = base64.b64decode(board.encode())
    return pickle.loads(board)


def board_full(board):
    """
    Checks that all of the positions are filled
    board: python_parsed board
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


def get_next_position(position, direction, board_size):
    """
    Given a position, find the next position in the given direction
    """
    pos_2d = (position % board_size, position // board_size)
    next_2d = list(map(add, pos_2d, direction))
    if (
        next_2d[0] >= board_size
        or next_2d[0] < 0
        or next_2d[1] >= board_size
        or next_2d[1] < 0
    ):
        return None
    else:
        return next_2d[1] * board_size + next_2d[0]


def scan(board, direction, position, player, count=0):
    """
    Scans the board in the given position until a None, an edge or a different player piece is found
    direction: 2d array that indicates the direction to scan. I.E. (1,1) is top right diagonal
    """
    board_size = int(
        len(board) ** 0.5
    )  # Board is always squared, so the sqrt of the length will give us the size
    next_position = get_next_position(position, direction, board_size)
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
