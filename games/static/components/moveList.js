class MoveItem extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    this.props.onReplay(this.props.value.id);
  }
  parseValue(value) {
    const match = /\[([0-6]),\ \'([R, L])\'\]/.exec(value);
    if (match) {
      return `${match[1]},${match[2]}`;
    }
  }
  render() {
    const parsed = this.parseValue(this.props.value.move);
    const date = new Date(this.props.value.timestamp);
    return React.createElement(
      "button",
      { className: "shadow p-2", onClick: this.handleClick },
      `${this.props.value.player_name}: ${parsed} - ${date.toLocaleString()}`
    );
  }
}

class MoveList extends React.Component {
  constructor(props) {
    super(props);
    this.handleReplay = this.handleReplay.bind(this);
  }
  handleReplay(id) {
    this.props.onReplay(id);
  }
  render() {
    const options = this.props.moves.map((child) => {
      return React.createElement(
        MoveItem,
        {
          key: `${child.timestamp}`,
          value: child,
          onReplay: this.handleReplay,
        },
        null
      );
    });
    const title = React.createElement(
      "h2",
      { key: "move-list-title", className: "p-2" },
      "Review Moves"
    );
    //options.unshift(title);
    React.createElement("div", { key: "move-list-title" }, title);
    const items = React.createElement(
      "div",
      {
        className: "p-2 h-64 overflow-scroll shadow flex flex-col",
        key: "move-list-items",
      },
      options
    );
    const cont = React.createElement("div", { className: "text-center" }, [
      title,
      items,
    ]);
    return cont;
  }
}
