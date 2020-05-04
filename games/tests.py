from django.test import TestCase
import random
import pickle
from games.board_utils import (
    pickle_board,
    generate_board,
    parse_board_from_string,
    board_full,
    scan,
    find_winner,
    get_next_position,
)
from games.move_utils import translate_move, apply_move
from games.models import Game, Move, BOARD_SIZE

# Create your tests here.
class GameModelTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_generate_board(self):
        """
        generate_board/1 returns a binary string representation with a board filled with 7*7 None values
        """
        board = generate_board(BOARD_SIZE)
        self.assertEqual(parse_board_from_string(board).count(None), 49)

    def test_generate_board_with_existing_board(self):
        """
        generate_board/1 parses board if one is passed, instead of generating a blank one
        """
        board = self.game.python_board
        board[0] = True
        board[10] = False
        board = pickle_board(board)
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

    def test_change_state_forward(self):
        """
        change_state_forward/3 persists the data to the database if the player and the move are valid
        """
        self.game.change_state_forward(True, (3, "R"))
        game = Game.objects.get(id=self.game.pk)
        self.assertTrue(game.python_board[27])
        self.game.change_state_forward(False, (3, "R"))
        game = Game.objects.get(id=self.game.pk)
        self.assertFalse(game.python_board[26])

    def test_change_state_forward_marks_finished_and_winner(self):
        """
        change_state_forward/3 marks the game as finished if there is a winner
        """
        board = ([True, False] * 25)[:49]
        board[0] = None
        self.game.board = pickle_board(board)
        self.game.save()
        self.game.change_state_forward(True, (0, "R"))
        game = Game.objects.get(id=self.game.pk)
        self.assertTrue(game.finished)
        self.assertTrue(game.winner)

    def test_change_state_forward_prevents_moves_when_finished(self):
        """
        change_state_forward/3 must not allow new moves after the game has been marked as finished
        """
        self.game.status = "FINISHED"
        self.game.save()
        self.game.change_state_forward(True, (0, "R"))
        self.assertIsNone(self.game.python_board[0])

    def test_change_state_marks_game_finished_when_no_moves_left(self):
        """
        change_state_forward/3 marks the game as finished when there are no movements left to be made
        """
        board = """[True, True, False, True, True, False, False,
                    True, False, True, False, True, False, True,
                    True, True, False, False, True, False, False,
                    False, True, False, True, False, True, False,
                    True, True, False, True, True, False, False,
                    False, False, True, False, True, True, True,
                    True, True, False, False, True, False, None]"""
        board = eval(board)
        self.game.board = pickle_board(board)
        self.game.save()
        self.game.change_state_forward(False, (6, "R"))
        game = Game.objects.get(id=self.game.id)
        self.assertEqual(game.status, "FINISHED")

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
        self.assertEqual(get_next_position(26, (-1, 0), BOARD_SIZE), 25),
        self.assertEqual(get_next_position(26, (-1, 1), BOARD_SIZE), 32),
        self.assertEqual(get_next_position(26, (-1, -1), BOARD_SIZE), 18),
        self.assertEqual(get_next_position(26, (1, 0), BOARD_SIZE), 27),
        self.assertEqual(get_next_position(26, (1, 1), BOARD_SIZE), 34),
        self.assertEqual(get_next_position(26, (1, -1), BOARD_SIZE), 20),
        self.assertEqual(get_next_position(26, (0, 1), BOARD_SIZE), 33),
        self.assertEqual(get_next_position(26, (0, -1), BOARD_SIZE), 19),

    def test_get_next_position_edges(self):
        """
        get_next_position/2 returns None if it reaches an edge
        """
        self.assertEqual(get_next_position(27, (1, 0), BOARD_SIZE), None)
        self.assertEqual(get_next_position(27, (1, 1), BOARD_SIZE), None)
        self.assertEqual(get_next_position(21, (-1, 0), BOARD_SIZE), None)
        self.assertEqual(get_next_position(21, (-1, -1), BOARD_SIZE), None)
        self.assertEqual(get_next_position(42, (1, 1), BOARD_SIZE), None)
        self.assertEqual(get_next_position(0, (1, -1), BOARD_SIZE), None)

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


class GameManagerTest(TestCase):
    def test_make_seat_finds_empty_seat(self):
        """
        make_seat/2 finds an empty seat if there is one
        """
        game = Game.objects.create(player_1="test1")
        found_game = Game.objects.make_seat("test2")
        self.assertEqual(found_game.player_2, "test2")
        self.assertEqual(found_game.id, game.id)

    def test_make_seat_creates_game(self):
        """
        make_seat/2 creates a new game if no empty seat is found
        """
        game = Game.objects.create(player_1="test1", player_2="test2")
        new_game = Game.objects.make_seat("test1")
        self.assertEqual(new_game.player_1, "test1")
        self.assertEqual(new_game.player_2, "")
        self.assertNotEqual(game.id, new_game)

    def test_find_game_no_active(self):
        """
        find_game/2 finds a suitable game to join for a given player if there is no active game
        """
        player_name = "player_1"
        new_game = Game.objects.find_game(player_name)
        self.assertEqual(new_game.player_1, player_name)
        self.assertEqual(new_game.player_2, "")

    def test_find_game_empty_seats(self):
        """
        find_game/2 finds a suitable game to join for a given player if there are games with empty seats 
        """
        player_name = "player_1"
        Game.objects.create(player_1="test")
        new_game = Game.objects.find_game(player_name)
        self.assertEqual(new_game.player_1, "test")
        self.assertEqual(new_game.player_2, player_name)

    def test_find_game_active_player_1(self):
        """
        find_game/2 finds a suitable game to join if the player is already participating in a game
        as player_1
        """
        player_name = "player_1"
        game = Game.objects.create(player_1=player_name, player_2="test")
        found_game = Game.objects.find_game(player_name)
        self.assertEqual(found_game.player_1, player_name)
        self.assertEqual(found_game.player_2, "test")
        self.assertEqual(found_game.id, game.id)

    def test_find_game_active_player_2(self):
        """
        find_game/2 finds a suitable game to join if the player is already participating in a game
        as player_1
        """
        player_name = "player_2"
        game = Game.objects.create(player_2=player_name, player_1="test")
        found_game = Game.objects.find_game(player_name)
        self.assertEqual(found_game.player_2, player_name)
        self.assertEqual(found_game.player_1, "test")
        self.assertEqual(found_game.id, game.id)
