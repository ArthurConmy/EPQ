# EPQ

This repository holds all important files in the EPQ qualification I am working towards. 

The following ReadMe also documents the development of all such files leading up to the penultimate product, that is, the Dots and Boxes player that beat me at the game.

# Simulator.py

In order to get to grips with the Dots and Boxes game, and in particular how the Python programming language facilitates this game, it is worth developing a simulator to play games of Dots and Boxes between several players (all human) and on arbitrarily sized grids.

```Python
board_size=4

hs=[0 for i in range(0, board_size*(board_size+1))]
vs=[0 for i in range(0, board_size*(board_size+1))]

no_players=2

our_completed_squares=[0 for i in range(0, no_players)]

players_turn=0
```
These 10 lines of code are the initialisation of a Dots and Boxes game. The variables defined are `board_size`, `hs`, `vs`, `no_players`, `our_completed_squares` and `players_turn`. Several are self-explanatory, but `hs` and `vs` are lists that store boolean values for whether each horizontal and vertical has been filled in. The reason for their abbreviated identifiers is their prevalence in the code, which means that it will be easier to code the rest of the program since typing will be faster.
