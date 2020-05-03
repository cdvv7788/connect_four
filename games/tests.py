from django.test import TestCase
import random
import pickle
from games.board_utils import (
    generate_board,
    parse_board_from_string,
    board_full,
    scan,
    find_winner,
    get_next_position,
)
from games.move_utils import translate_move, apply_move
from games.models import Game, Move

# Create your tests here.
class GameModelTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_generate_board(self):
        """
        generate_board/1 returns a binary string representation with a board filled with 7*7 None values
        """
        board = generate_board()
        self.assertEqual(parse_board_from_string(board).count(None), 49)

    def test_generate_board_with_existing_board(self):
        """
        generate_board/1 parses board if one is passed, instead of generating a blank one
        """
        board = self.game.python_board
        board[0] = True
        board[10] = False
        board = generate_board(board)
        self.assertEqual(parse_board_from_string(board).count(True), 1)
        self.assertEqual(parse_board_from_string(board).count(False), 1)
        self.assertEqual(parse_board_from_string(board).count(None), 47)

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

    def test_add_move(self):
        """
        add_move/3 persists the data to the database if the player and the move are valid
        """
        self.game.add_move(True, (3, "R"))
        game = Game.objects.get(id=self.game.pk)
        self.assertTrue(game.python_board[27])
        self.game.add_move(False, (3, "R"))
        game = Game.objects.get(id=self.game.pk)
        self.assertFalse(game.python_board[26])

    def test_add_move_marks_finished_and_winner(self):
        """
        add_move/3 marks the game as finished if there is a winner
        """
        board = ([True, False] * 25)[:49]
        board[0] = None
        self.game.board = generate_board(board)
        self.game.save()
        self.game.add_move(True, (0, "R"))
        game = Game.objects.get(id=self.game.pk)
        self.assertTrue(game.finished)
        self.assertTrue(game.winner)

    def test_add_move_prevents_moves_when_finished(self):
        """
        add_move/3 must not allow new moves after the game has been marked as finished
        """
        self.game.finished = True
        self.game.save()
        self.game.add_move(True, (0, "R"))
        self.assertIsNone(self.game.python_board[0])

    def test_apply_move_raises_key_error(self):
        """
        When the movement is not possible, this method will raise a TypeError
        This can be improved later, but for now it will suffice
        """
        board = self.game.python_board
        with self.assertRaises(TypeError):
            apply_move(board, False, (1, "R"))

    def test_apply_move_works_with_valid_move(self):
        """
        When a board and a valid move for that given board is sent, a new board with
        the applied move is returned
        """
        board = self.game.python_board
        self.assertTrue(apply_move(board, True, (1, "R"))[13])

    def test_get_next_position(self):
        """
        get_next_position/2 returns the next position in the array to check
        """
        self.assertEqual(get_next_position(26, (-1, 0)), 25),
        self.assertEqual(get_next_position(26, (-1, 1)), 32),
        self.assertEqual(get_next_position(26, (-1, -1)), 18),
        self.assertEqual(get_next_position(26, (1, 0)), 27),
        self.assertEqual(get_next_position(26, (1, 1)), 34),
        self.assertEqual(get_next_position(26, (1, -1)), 20),
        self.assertEqual(get_next_position(26, (0, 1)), 33),
        self.assertEqual(get_next_position(26, (0, -1)), 19),

    def test_get_next_position_edges(self):
        """
        get_next_position/2 returns None if it reaches an edge
        """
        self.assertEqual(get_next_position(27, (1, 0)), None)
        self.assertEqual(get_next_position(27, (1, 1)), None)
        self.assertEqual(get_next_position(21, (-1, 0)), None)
        self.assertEqual(get_next_position(21, (-1, -1)), None)
        self.assertEqual(get_next_position(42, (1, 1)), None)
        self.assertEqual(get_next_position(0, (1, -1)), None)

    def test_scan_counts_properly(self):
        """
        scan/5 retrieves the count in the given direction until it finds an
        edge or another player turn
        """
        board = """[
            False, False, False, True, True, None, None,
            False, False, True, True, None, True, False,
            False, True, True, True, True, None, None,
            False, False, True, False, None, None, None,
            False, True, False, True, None, None, None,
            True, True, False, None, True, None, None,
            False, True, False, None, True, None, None,
            True, False, False, None, None, None, None,
        ]"""
        board = eval(board)
        self.assertEqual(scan(board, (0, 1), 14, False), 2)
        self.assertEqual(scan(board, (0, -1), 14, False), 2)
        self.assertEqual(scan(board, (1, 0), 15, True), 3)
        self.assertEqual(scan(board, (-1, 1), 4, True), 2)
        self.assertEqual(scan(board, (-1, 1), 44, False), 0)
        self.assertEqual(scan(board, (1, 1), 14, False), 2)

    def test_find_winner(self):
        """
        find_winner/2 returns the winner if there are 4 in a row
        """

        board = """[
            False, False, False, True, True, None, None,
            False, False, True, True, None, True, False,
            False, True, True, True, True, None, None,
            False, False, True, False, None, None, None,
            False, True, False, True, None, None, None,
            True, True, False, None, True, None, None,
            False, True, False, None, True, None, None,
            True, False, False, None, None, None, None,
        ]"""
        board = eval(board)
        player_1 = True
        player_2 = False
        self.assertEqual(find_winner(board, 28), player_2)
        self.assertEqual(find_winner(board, 35), player_1)
        self.assertEqual(find_winner(board, 16), player_1)
        self.assertEqual(find_winner(board, 31), player_1)
        self.assertEqual(find_winner(board, 39), player_1)
        self.assertEqual(find_winner(board, 43), None)


class MoveModelTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_moves_are_retrieved_in_desc_order(self):
        """
        When querying moves, they must be ordered in descending order by default
        by the timestamp field (newest first)
        """
        moves = map(
            lambda x: Move.objects.create(game=self.game, move=(x, "R")), range(3)
        )
        filtered_moves = Move.objects.filter(game=self.game)
        for i in range(len(filtered_moves)):
            self.assertEqual(moves[i].id, filtered_moves[i].id)
