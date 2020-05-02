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
      "button",
      { onClick: this.handleClick },
      this.props.direction == "L" ? "->" : "<-"
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
        },
        child
      );
    });
    return React.createElement("div", { className: "flex flex-col" }, children);
  }
}
