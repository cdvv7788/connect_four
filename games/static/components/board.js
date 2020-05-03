/**
 * Given an element, defines what character to return
 */
function parseElement(element) {
  let props;
  switch (element) {
    case true:
      props = { className: "dot bg-blue-600" };
      break;
    case false:
      props = { className: "dot bg-red-600" };
      break;
    default:
      props = { className: "dot bg-green-100" };
  }
  return React.createElement("span", props, null);
}

function BoardState(props) {
  if (props.board) {
    let items = [];
    for (i = 0; i < props.board.length; i++) {
      items.push(
        React.createElement(
          "div",
          {
            className: "bg-red-100 rounded-full",
            key: `element-${i}`,
          },
          parseElement(props.board[i])
        )
      );
    }
    return React.createElement(
      "div",
      {
        className:
          "grid grid-flow-row grid-cols-7 grid-rows-7 gap-2 bg-green-500 p-5 rounded-lg leading-null",
      },
      items
    );
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
      {
        board: this.props.board,
        key: "board-state",
        className: "bg-green-500",
      },
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
