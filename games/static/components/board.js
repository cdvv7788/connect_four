function Board(props) {
  if (props.board) {
    let output = "";
    for (var i = 0; i < props.board.length; i++) {
      if (i % 7 == 0) {
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
