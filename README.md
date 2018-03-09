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

The looping structure for the program is not particularly complex it is essentially a `while True:` loop, but not exactly this since we would like to be able to know which turn of the game it is. Instead

```Python

from itertools import count 

## ... things

for turn in count(1):

  ## each turn of the game
```

creates a variable `turn` that is the turn of the game for which a move is being made. The first piece of code inside this `for` loop is

``` Python
print_game(vs, hs, board_size)
```

which calls the function

``` Python
def print_game(verticals, horizontals, bs): ## Takes input as the horizontals and verticals of the game. Prints the board. Doesn't account for drawing letters in squares that have been won
  
    for index in range(0, bs+1):
        for index_2 in range(index*bs, index*bs + bs):
            if horizontals[index_2]==1:
                print('{} --'.format(white), end='')
            else:
                print('{} --{}'.format(black, reset), end='') ## colour ?!
        print()
        if index!=bs:
            for index_3 in range(index*(bs+1), index*(bs+1) + bs + 1):
                if verticals[index_3]==1:
                    print('{}|  {}'.format(white, reset), end='')
                else:
                    print('{}|  {}'.format(black, reset), end='')
        print()
```

