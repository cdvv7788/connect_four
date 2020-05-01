function BoardState(props) {
  if (props.board) {
    let output = "";
    for (var i = 0; i < props.board.length; i++) {
      if (i % 7 == 0 && i != 0) {
        output = output + "\n";
      }
      output += ` ${
        props.board[i] ? "X" : props.board[i] === false ? "O" : "-"
      } `;
    }
    return React.createElement("pre", { className: "text-center p-4" }, output);
  }
  return "";
}

function Board(props) {
  const boardState = React.createElement(
    BoardState,
    { board: props.board, key: "board-state" },
    null
  );
  const leftPicker = React.createElement(
    Picker,
    { position: "L", key: "picker-l" },
    null
  );
  const rightPicker = React.createElement(
    Picker,
    { position: "R", key: "picker-r" },
    null
  );
  return React.createElement(
    "div",
    { className: "flex flex-row items-center justify-center" },
    [leftPicker, boardState, rightPicker]
  );
}
