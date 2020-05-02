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
      const currentPlayer = data["next_player"] ? "player_1" : "player_2";

      if (!data.started) {
        component.setState({
          message: "Awaiting for another player to start the game...",
        });
      } else if (data["finished"]) {
        const winner_message = data["winner"]
          ? `The winner is player 1: ${data["player_1"]}`
          : data["winner"] === false
          ? `The winner is player 2: ${data["player_2"]}`
          : "This game was a draw.";
        component.setState({
          message: `This game has finished. ${winner_message}`,
        });
      } else {
        // Game in progress
        if (data[currentPlayer] === component.props.username) {
          component.setState({
            message: "It is your turn to make a move!",
          });
        } else {
          component.setState({
            message: `Now it is ${currentPlayer}'s turn`,
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
      { message: this.state.message, key: "message" },
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
      { message: `Playing as: ${this.props.username}`, key: "current-player" },
      null
    );
    return [message, board, currentPlayer];
  }
}
