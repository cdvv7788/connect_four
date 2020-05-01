class PickerButton extends React.Component {
  render() {
    return React.createElement(
      "div",
      {},
      this.props.direction == "L" ? "->" : "<-"
    );
  }
}

class Picker extends React.Component {
  render() {
    let children = [...Array(7).keys()].map((child) => {
      return React.createElement(
        PickerButton,
        {
          key: `${this.props.position}-${child}`,
          position: child,
          direction: this.props.position,
        },
        child
      );
    });
    return React.createElement("div", {}, children);
  }
}
