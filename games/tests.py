from django.test import TestCase
import random
from games.models import (
    Game,
    generate_blank_board,
    parse_board_from_string,
    board_full,
    translate_move,
)

# Create your tests here.
class GameModelTest(TestCase):
    def setUp(self):
        self.game = Game()

    def test_generate_blank_board(self):
        """
        generate_blank_board/0 returns a str with a board filled with 7*7 None values
        """
        board = generate_blank_board()
        self.assertEqual(board.count("None"), 49)

    def test_parse_board_from_string(self):
        """
        parse_board_from_string/1 returns a python list of len 7*7 given a game board
        """
        parsed = parse_board_from_string(self.game.board)
        self.assertEqual(len(parsed), 49)

    def test_board_full(self):
        """
        board_full/1 checks if the board is completely filled
        """
        self.assertFalse(board_full(self.game.python_board))
        board = self.game.python_board
        sample = [True, False]
        for i in range(len(board)):
            board[i] = random.sample(sample, 1)[0]
        self.assertTrue(board_full(board))

    def test_translate_move_fails_when_not_player_turn(self):
        """
        translate_move/3 returns None when the wrong player is trying to make a move
        """
        player_2 = False
        new_index = translate_move(self.game.python_board, player_2, (3, "R"))
        self.assertTrue(new_index is None)

    def test_translate_move_succeeds_when_player_turn(self):
        """
        translate_move/3 returns the index for the move when it is a valid move
        """
        player_1 = True
        new_index = translate_move(self.game.python_board, player_1, (3, "L"))
        self.assertTrue(type(new_index) is int)

    def test_translate_move_fails_when_board_is_full(self):
        """
        translate_move/3 returns None when it does not find a place to stack a new piece
        """
        board = ([True, False] * 25)[:49]
        new_index = translate_move(board, True, (3, "L"))
        self.assertTrue(new_index is None)
