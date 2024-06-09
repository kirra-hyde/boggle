"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

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

async function playWord(evt) {
  evt.preventDefault();
  $message.empty();
  const word = $wordInput.val();
  const resp = await axios.post("/api/score-word", {word: word, gameId: gameId});
  if (resp.data.result !== "ok") {
    $message.text("Not a valid word on the board");
  } else {
    $playedWords.append(`<li>${word}</li>`);
  }
}

$form.on("submit", playWord);

start();