# Connect Four

## About

The project is a connect_four variant, where the plays are not made from the top, but they are stacked from the sides.

This projects implements the game logic in Django, using 2 models for this:

- Game: Holds the game state
- Move: Holds every move that has been performed in a given game

There is a very basic matchmaking. When you access the root of the site (`/`) and you input a name, it will try to find a game with an empty seat. If there is none, a new game will be created and the player will have to wait until a new player comes by.

Once both players are ready to get started, you can start adding pieces by clicking the arrows to the sides of the board. Once someone wins (4 connected pieces) the message will change to notify this.

A list of all of the moves performed up to date is to the right side of the board.

This game uses websockets to coordinate both clients.

## How to run the project

To start the game, you will need [Docker Compose](https://docs.docker.com/compose/).

Once you have it installed, you need to create a `.env` file at the root:

```
SECRET_KEY="my_secret_key"
```

After that, running the following command should suffice:

```
make compose
```

Now you should be able to access the game by going to `http://localhost:9000`
