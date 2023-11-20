# Tic Cat Toe

Have you ever wanted to play Tic Tac Toe when you was a kid but you had no one to play with?
The Cheshire cat is here to make those times just a memory! Play one of the most famous childhood games with the friendly Cheshire Cat.

## Usage

1. Install the plugin and
2. have fun!

## Notes

The plugin is to be used just to play tic-tac-toe with the Cat, so, it starts with something like:
```
Let's play tic tac toe!
```

When the cat asks you which mark you want to use, "X" or "O", you need to use capital letter, since the code needs to set
the player's signs, and currently it is hardcoded that way.

When the cat asks you who wanna start first, you need to answer with something that contains "me" or "you".

I know, it's ugly but the main reason behind this plugin was mainly to play with the hooks and explore their power!

Let the hook be with you!

## disclaimer

The game starts only when marks are assigned, together with who starts the first mark placement. Once a round is finished, game status is reset, so asking for another round of tic-tac-toe brings to another match.
It might happen that the cat forgets to ask signs/who starts first, just tell the Cat and it will manage it.

## Todos

- Improve code
- Add a game global state
- Add some checks on user input (for example, choosing a number greater than 9, not a thing in a 3x3 Tic Tac Toe game)