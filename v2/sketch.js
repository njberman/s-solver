function copyArray(array) {
  return array.map((row) => row.slice());
}

let sudoku = Array.from({ length: 9 }, () =>
  Array.from({ length: 9 }, () => 0),
);
let possibles = Array.from(
  { length: 9 },
  () => Array.from({ length: 9 }),
  () => [],
);
// Easy sudoku:
// sudoku = [
//   [8, 0, 1, 3, 4, 0, 0, 2, 0],
//   [0, 5, 0, 6, 0, 0, 8, 0, 3],
//   [0, 0, 0, 0, 9, 5, 1, 0, 0],
//   [6, 0, 0, 0, 5, 9, 0, 0, 4],
//   [0, 0, 3, 0, 0, 0, 7, 5, 0],
//   [0, 0, 5, 2, 3, 0, 6, 8, 0],
//   [0, 0, 9, 5, 0, 8, 4, 0, 6],
//   [5, 7, 0, 1, 0, 0, 2, 0, 8],
//   [3, 0, 6, 0, 0, 0, 0, 0, 0],
// ];
// Extreme sudoku:
// sudoku = [
//   [6, 0, 0, 7, 9, 0, 2, 0, 8],
//   [0, 0, 0, 0, 0, 0, 3, 0, 0],
//   [0, 4, 0, 6, 0, 0, 0, 0, 0],
//   [0, 5, 0, 0, 0, 2, 8, 0, 7],
//   [8, 0, 0, 0, 0, 0, 0, 3, 0],
//   [0, 0, 0, 0, 7, 0, 0, 4, 0],
//   [4, 0, 0, 0, 2, 0, 6, 0, 9],
//   [0, 0, 1, 0, 0, 5, 0, 0, 0],
//   [0, 0, 0, 0, 0, 0, 0, 7, 0],
// ];
// Supposedly un-bruteforceable (btw, it did manage to solve it, took it like 9~10 mins, on the second time took 15 mins):
// sudoku = [
//   [0, 0, 0, 0, 0, 0, 0, 0, 0],
//   [0, 0, 0, 0, 0, 3, 0, 8, 5],
//   [0, 0, 1, 0, 2, 0, 0, 0, 0],
//   [0, 0, 0, 5, 0, 7, 0, 0, 0],
//   [0, 0, 4, 0, 0, 0, 1, 0, 0],
//   [0, 9, 0, 0, 0, 0, 0, 0, 0],
//   [5, 0, 0, 0, 0, 0, 0, 7, 3],
//   [0, 0, 2, 0, 1, 0, 0, 0, 0],
//   [0, 0, 0, 0, 4, 0, 0, 0, 9],
// ];
const hard = copyArray(sudoku);

let savedStates = [];

let listeningForNumber = false;

let solving = false;

function backprop() {
  const {
    sudoku: prevSudoku,
    possibles: prevPossibles,
    i: y,
    j: x,
    tried,
  } = savedStates[savedStates.length - 1];

  if (tried.length === prevPossibles[y][x].length) {
    savedStates.pop();
    return backprop();
  }

  let newRandomIndex = 0;
  while (true) {
    newRandomIndex = Math.floor(Math.random() * possibles[y][x].length);
    if (!tried.includes(newRandomIndex)) break;
  }

  sudoku = copyArray(prevSudoku);
  sudoku[y][x] = prevPossibles[y][x][newRandomIndex];
  savedStates[savedStates.length - 1].tried.push(newRandomIndex);
  return;
}

function setup() {
  createCanvas(600, 600);
  textFont("Courier New");
  textAlign(CENTER, CENTER);
}

function draw() {
  background(0);
  translate(50, 50);

  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      if (sudoku[i][j] !== 0) continue;
      possibles[i][j] = possible(sudoku, i, j);
    }
  }

  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      if (sudoku[i][j] === 0 && possibles[i][j].length === 0) {
        return backprop();
      }
    }
  }

  stroke(255);
  for (let i = 0; i < 10; i++) {
    if (i % 3 === 0) strokeWeight(3);
    else strokeWeight(1);
    line((i * 500) / 9, 0, (i * 500) / 9, 500);
    line(0, (i * 500) / 9, 500, (i * 500) / 9);
  }

  fill(255);
  noStroke();
  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      textSize(30);
      text(
        sudoku[i][j] !== 0 ? sudoku[i][j] : "",
        250 / 9 + (j * 500) / 9,
        250 / 9 + (i * 500) / 9,
      );

      // if (sudoku[i][j] !== 0) continue;
      // textSize(15);
      // for (let n = 0; n < possibles[i][j].length; n++) {
      //   text(possibles[i][j][n], 100/9 + j * 500/9 + 10 * n, 100/9 + i * 500/9);
      // }
    }
  }

  if (withInSudoku()) {
    noFill();
    stroke(200);
    rect(
      (Math.floor((mouseX - 50) / (500 / 9)) * 500) / 9,
      (Math.floor((mouseY - 50) / (500 / 9)) * 500) / 9,
      500 / 9,
      500 / 9,
    );
  }

  if (listeningForNumber) {
    noFill();
    stroke(255);
    rect(
      (listeningForNumber.j * 500) / 9,
      (listeningForNumber.i * 500) / 9,
      500 / 9,
      500 / 9,
    );
  }

  if (solving) solve();
}

function withInSudoku() {
  return 50 < mouseX && mouseX < 550 && 50 < mouseY && mouseY < 550;
}

function mousePressed() {
  if (withInSudoku()) {
    listeningForNumber = {
      i: Math.floor((mouseY - 50) / (500 / 9)),
      j: Math.floor((mouseX - 50) / (500 / 9)),
    };
  } else {
    listeningForNumber = false;
  }
}

function keyPressed() {
  if (
    0 <= parseInt(key) &&
    parseInt(key) <= 9 &&
    listeningForNumber !== false
  ) {
    const { i, j } = listeningForNumber;
    sudoku[i][j] = parseInt(key);
    listeningForNumber = false;
  }

  if (key === "s") {
    console.log(sudoku);
  }

  if (key === " ") {
    // solve();
    solving = !solving;
  }
}

function possible(s, i, j) {
  const row = s[i];

  let col = [];
  for (let y = 0; y < 9; y++) {
    col.push(s[y][j]);
  }

  let square = [];
  for (let y = Math.floor(i / 3) * 3; y < Math.floor(i / 3) * 3 + 3; y++) {
    for (let x = Math.floor(j / 3) * 3; x < Math.floor(j / 3) * 3 + 3; x++) {
      square.push(s[y][x]);
    }
  }

  let notPossible = row.concat(col).concat(square);
  notPossible = [...new Set(notPossible)].sort();

  let possible = [];

  for (let n = 1; n <= 9; n++) {
    if (!notPossible.includes(n)) possible.push(n);
  }

  return possible;
}

function solve(n) {
  if (sudoku.every((row) => row.every((val) => val !== 0))) {
    console.log("It's solved mate, you can stop now!");
    return;
  }

  if (n === undefined) n = 1;
  for (let i = 0; i < 9; i++) {
    for (let j = 0; j < 9; j++) {
      if (sudoku[i][j] === 0 && possibles[i][j].length === n) {
        let index = Math.floor(Math.random() * (n - 1));

        if (n > 1) {
          savedStates.push({
            sudoku: copyArray(sudoku),
            possibles: copyArray(possibles),
            i,
            j,
            tried: [index],
          });
        }
        sudoku[i][j] = possibles[i][j][index];
        return;
      }
    }
  }

  return solve(n + 1);
}
