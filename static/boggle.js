"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $wordScore = $("#word-score");
const $totalScore = $("#total-score");
const $highScore = $("#high-score");
const $timer = $("#timer");
const $end = $("#end-message");
const $restart = $("#restart");

let gameId;
// How many seconds a game will last
const GAME_LENGTH = 180
let seconds = GAME_LENGTH;

/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  const { board } = response.data;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  const $body = $("<tbody>");
  for (let row of board) {
    const $row = $("<tr>");
    for (let cell of row) {
      const $cell = $(`<td>${cell}</td>`);
      $row.append($cell);
    }
    $body.append($row);
  }
  $table.append($body);
}

/** Get word from form and submit it to API to be played */

async function playWord(evt) {
  evt.preventDefault();
  $message.empty();
  $wordScore.text(" ");
  const word = $wordInput.val().toUpperCase();
  $wordInput.val("");
  const resp = await axios.post("/api/score-word", {word: word, gameId: gameId});
  const { result, score, totalScore } = resp.data;
  showWord(word, result)
  if (score && totalScore) {
    showScore(score, totalScore);
  }
}

/** Add word to word list, if valid, or else display error message */

function showWord(word, result) {
  if (result === "ok") {
    $playedWords.append(`<li>${word}</li>`);
    return;
  }

  $message.show();
  if (result === "not-word") {
    $message.text("Not a valid word");
  } else if (result === "not-on-board") {
    $message.text("Word not on board");
  } else if (result === "duplicate") {
    $message.text("You already played this");
  }
  setTimeout(() => {$message.hide()}, 1500)
}

/** Show word score and show updated total score */

function showScore(wordScore, totalScore) {

  if (wordScore === 1) {
    $wordScore.text("1 point!");
  } else {
    $wordScore.text(`${wordScore} points!`);
  }

  $totalScore.text(`Score: ${totalScore}`);
  setTimeout(() => {$wordScore.text("")}, 1500);
}

$form.on("submit", playWord);

/** Decrement time and have clock updated */

function reduceTime() {
  seconds--;
  updateTimeDisplay();
  if (seconds === 0) {
    clearInterval(intervalId);
    $form.hide();

    endGame();
  }
}

/** Have high score updated, show end message and restart button */

async function endGame() {
  const resp = await axios.post("/api/end-game", {id: gameId});

  const { score } = resp.data;
  $end.text(`It's over! Score: ${score}`);

  $restart.show();
    $restart.on("click", () => {
      location.reload();
    });
}

/** Update timer display */

function updateTimeDisplay() {
  const hour = Math.floor(seconds / 60);
  let minutes = seconds % 60;
  minutes = minutes.toString().padStart(2, "0");
  $timer.text(`${hour}:${minutes}`);
}

const intervalId = setInterval(reduceTime, 1000);

start();