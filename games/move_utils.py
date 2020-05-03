import copy
from .board_utils import next_turn


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
    board_size = int(len(board) ** 0.5)
    if next_turn(board) == player:
        offset = move[0] * board_size
        direction = (
            range(offset, offset + board_size)
            if move[1] == "L"
            else range(offset + board_size - 1, offset - 1, -1)
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
