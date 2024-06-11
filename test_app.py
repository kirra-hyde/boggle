from unittest import TestCase

from app import app, games
from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            resp = client.post("/api/new-game")
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            board = data["board"]
            game_id = data["gameId"]
            self.assertIsInstance(game_id, str)
            self.assertIsInstance(board, list)
            self.assertIsInstance(board[0], list)
            self.assertIsInstance(board[0][0], str)

            self.assertIsInstance(games[game_id], BoggleGame)

    def test_score_word(self):
        """Test scoring a word"""

        with self.client as client:
            resp = client.post("/api/new-game")
            id = resp.get_json()["gameId"]
            game = games[id]
            game.board = [["C", "A", "T"],["X", "X", "S"],["X", "X", "X"]]

            good_resp = client.post(
                "/api/score-word", json={"word": "cat", "gameId": id}
            )
            good_data = good_resp.get_json()

            self.assertEqual(good_data, {"result": "ok", "score": 1, "totalScore": 1})

            good_resp_2 = client.post(
                "/api/score-word", json={"word": "cats", "gameId": id}
            )
            good_data_2 = good_resp_2.get_json()

            self.assertEqual(good_data_2, {"result": "ok", "score": 1, "totalScore": 2})

            dup_resp = client.post(
                "/api/score-word", json={"word": "cat", "gameId": id}
            )
            dup_data = dup_resp.get_json()

            self.assertEqual(dup_data, {"result": "duplicate"})

            resp_invalid_word = client.post(
                "/api/score-word", json={"word": "tac", "gameId": id}
            )
            invalid_word_data = resp_invalid_word.get_json()

            self.assertEqual(invalid_word_data, {"result": "not-word"})

            resp_not_on_board = client.post(
                "/api/score-word", json={"word": "dog", "gameId": id}
            )
            not_on_board_data = resp_not_on_board.get_json()

            self.assertEqual(not_on_board_data, {"result": "not-on-board"})