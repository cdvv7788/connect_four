class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = { message: "Game is loading...", moves: [] };
    this.handleMove = this.handleMove.bind(this);
  }
  handleMove(move) {
    this.props.gameSocket.send(
      JSON.stringify({
        move: move.split(","),
        player: this.props.username,
      })
    );
  }
  componentDidMount() {
    const component = this;
    this.props.gameSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      const currentPlayer = data["next_player"]
        ? data["player_1"]
        : data["player_2"];

      switch (data.status) {
        case "PENDING":
          component.setState({
            message: "Awaiting for another player to start the game...",
          });
          break;
        case "FINISHED":
          const winner_message = data["winner"]
            ? `The winner is player 1: ${data["player_1"]}`
            : data["winner"] === false
            ? `The winner is player 2: ${data["player_2"]}`
            : "This game was a draw.";
          component.setState({
            message: `This game has finished. ${winner_message}`,
          });
          break;
        default:
          // Game in progress
          if (currentPlayer === component.props.username) {
            component.setState({
              message: "It is your turn to make a move!",
              messageColor: "green",
            });
          } else {
            component.setState({
              message: `Now it is ${currentPlayer}'s turn`,
              messageColor: "red",
            });
          }
      }
      component.setState({ board: data.board, moves: data.moves });
    };
    this.props.gameSocket.onclose = function (e) {
      console.error("Game socket closed unexpectedly");
    };
  }
  render() {
    const message = React.createElement(
      Message,
      {
        message: this.state.message,
        messageColor: this.state.messageColor,
        key: "message",
      },
      null
    );
    const board = React.createElement(
      Board,
      {
        board: this.state.board,
        key: "board",
        onMove: this.handleMove,
        moves: this.state.moves,
      },
      null
    );
    const currentPlayer = React.createElement(
      Message,
      {
        message: `Playing as: ${this.props.username}`,
        key: "current-player",
        messageColor: this.props.messageColor,
      },
      null
    );
    const moveList = React.createElement(
      MoveList,
      { key: "move-list", moves: this.state.moves },
      null
    );
    return [message, board, currentPlayer, moveList];
  }
}
