from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame
from wordlist import english_words

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """Check that word is valid and on board"""

    word = request.json["word"].upper()
    id = request.json["gameId"]
    game = games[id]

    if not game.is_word_in_word_list(word):
       return jsonify({"result": "not-word"})

    if not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    score = game.play_and_score_word(word)
    return jsonify({"result": "ok", "score": score})


