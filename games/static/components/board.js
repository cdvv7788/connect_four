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

class Board extends React.Component {
  constructor(props) {
    super(props);
    this.handleMove = this.handleMove.bind(this);
  }
  handleMove(move) {
    this.props.onMove(move);
  }
  render() {
    const boardState = React.createElement(
      BoardState,
      { board: this.props.board, key: "board-state" },
      null
    );
    const leftPicker = React.createElement(
      Picker,
      { position: "L", key: "picker-l", onMove: this.handleMove },
      null
    );
    const rightPicker = React.createElement(
      Picker,
      { position: "R", key: "picker-r", onMove: this.handleMove },
      null
    );
    return React.createElement(
      "div",
      { className: "flex flex-row items-center justify-center" },
      [leftPicker, boardState, rightPicker]
    );
  }
}
