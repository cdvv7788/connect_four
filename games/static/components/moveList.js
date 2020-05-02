class MoveItem extends React.Component {
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
      { className: "shadow p-2" },
      `${this.props.value.player_name}: ${parsed} - ${date.toLocaleString()}`
    );
  }
}

class MoveList extends React.Component {
  render() {
    let options = this.props.moves.map((child) => {
      return React.createElement(
        MoveItem,
        {
          key: `${child.timestamp}`,
          value: child,
        },
        null
      );
    });
    const title = React.createElement(
      "h2",
      { key: "move-list-title", className: "p-2 ml-10" },
      "Move List"
    );
    //options.unshift(title);
    React.createElement("div", {}, title);
    const items = React.createElement(
      "div",
      {
        className:
          "ml-10 p-2 h-64 overflow-scroll shadow flex flex-col text-center",
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
