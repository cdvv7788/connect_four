from django.test import TestCase
import random
from games.models import Game, generate_blank_board, parse_board_from_string, board_full

# Create your tests here.
class GameTest(TestCase):
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
