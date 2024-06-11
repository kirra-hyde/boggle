from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    high_score = session.get("high_score", 0)

    return render_template("index.html", high_score=high_score)


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
    """Check that word is valid and on board. Play and score the word."""

    word = request.json["word"].upper()
    id = request.json["gameId"]
    game = games[id]

    if not game.is_word_in_word_list(word):
       return jsonify({"result": "not-word"})

    if not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    if not game.is_word_not_a_dup(word):
        return jsonify({"result": "duplicate"})

    score = game.play_and_score_word(word)
    return jsonify({"result": "ok", "score": score, "totalScore": game.score})

@app.post("/api/end-game")
def end_game():
    """Update high score at end of game"""

    high_score = session.get("high_score", 0)
    id = request.json["id"]
    game = games[id]

    if game.score > high_score:
        session["high_score"] = game.score
        return jsonify({"updated": True, "score": game.score})
    else:
        return jsonify({"updated": False, "score": game.score})



