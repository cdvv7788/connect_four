class PickerButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    this.props.onMove(this.props.move);
  }
  render() {
    return React.createElement(
      "span",
      {
        onClick: this.handleClick,
        className: "dot dot-hover bg-green-500 p-5 rounded-lg leading-null",
      },
      null
    );
  }
}

class Picker extends React.Component {
  constructor(props) {
    super(props);
    this.handleMove = this.handleMove.bind(this);
  }
  handleMove(move) {
    this.props.onMove(move);
  }
  render() {
    let children = [...Array(7).keys()].map((child) => {
      return React.createElement(
        PickerButton,
        {
          key: `${this.props.position},${child}`,
          move: `${child},${this.props.position}`,
          direction: this.props.position,
          onMove: this.handleMove,
          className: "dot bg-yellow-800 p-5",
        },
        child
      );
    });
    return React.createElement(
      "div",
      {
        className:
          "grid grid-flow-row grid-cols-1 grid-rows-7 gap-2 p-2 bg-green-400",
      },
      children
    );
  }
}
