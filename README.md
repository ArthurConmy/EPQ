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
def print_game(verticals, horizontals, bs):
  
    for index in range(0, bs+1):
        for index_2 in range(index*bs, index*bs + bs):
            if horizontals[index_2]==1:
                print('{} --', end='')
            else:
                print('{}   {}', end='')
        print()
        if index!=bs:
            for index_3 in range(index*(bs+1), index*(bs+1) + bs + 1):
                if verticals[index_3]==1:
                    print('{}|  {}'), end='')
                else:
                    print('{}   {}', end='')
        print()
```

which takes the arguments `verticals`, `horizontals` and `bs`, that being the board size of the grid. I tested this function yet found it to be unsatisfactory, especially for large grids; since it is ambiguous as to which line in the grid has been shaded:

INSERT IMAGE

Instead, the following redefinition of `print_game` allows for the lines in the grid yet to be filled in to be coloured in a much darker shade, yet their presence is still definite

``` Python
def print_game(verticals, horizontals, bs): 

    for index in range(0, bs+1):
        for index_2 in range(index*bs, index*bs + bs):
            if horizontals[index_2]==1:
                print('{} --'.format(white), end='')
            else:
                print('{} --{}'.format(black, reset), end='')
        print()
        if index!=bs:
            for index_3 in range(index*(bs+1), index*(bs+1) + bs + 1):
                if verticals[index_3]==1:
                    print('{}|  {}'.format(white, reset), end='')
                else:
                    print('{}|  {}'.format(black, reset), end='')
        print()
```

And within a game on repl.it:

INSERT IMAGE

There is only one more function that must be defined, that is `completed_squares`, that returns the number of completed squares in a given grid within a Dots and Boxes game. This is important for two reasons: it allows us to determine when the turn does not change, i.e, when a player gets another go after they complete a box in a game, and it also allows us to determine who has won the game at its end, by comparing the number of sqaures that each player has won.

```Python
def completed_squares(verticals, horizontals, bs):

    the_completed_squares=[]
    
    for upper in range(0, len(horizontals)-bs): 
        if horizontals[upper]==1: 
            if horizontals[upper+bs]==1:
                if verticals[upper + upper//bs]==1: 
                    if verticals[upper + upper//bs + 1]==1:
                        the_completed_squares.append(upper)
                
    return len(the_completed_squares)
```
With all necessary functions defined, the remaining code to simulate a game of Dots and Boxes is very brief:

``` Python
for turn in count(1):
  
  ## FIRST STAGE
  
  print_game(vs, hs, board_size)
  
  ## SECOND STAGE
  
  move_made=input('Player '+str(players_turn+1)+' Enter your move')
  move_made=[move_made[0], int(move_made[1:])]
    
  if move_made[0]=='h':
    hs[move_made[1]]=1
    
  if move_made[0]=='v':
    vs[move_made[1]]=1

  ## THIRD STAGE

  if completed_squares(vs, hs, board_size) > sum(our_completed_squares):
    print('Player', players_turn+1, 'takes', completed_squares(vs, hs, board_size)-sum(our_completed_squares), 'square(s)! They get another go!')
    our_completed_squares[players_turn]+=completed_squares(vs, hs, board_size)-sum(our_completed_squares)
  
  else:
    players_turn+=1
    players_turn=players_turn%2
```

There are essentially three stages to the turn loop: the first stage is to call `print_game` and print out the current state of the board. This comes first because it allows the player entering their move to see the board that they are making a move on, which is very important because of the somewhat unintuitive input format.

Secondly, the move input is taken and then acted upon: the corresponding index of `vs` or `hs` is turned from `0`, representing 'false' to `1`, representing 'true'.

Thirdly and finally, `our_completed_squares` is updated based upon whether any new squares have been formed, this of course being determined from the output of the `completed_squares` function. If squares have not been won, then the turn is rotated to the other player.

The final part of the code is as follows

``` Python
  if vs.count(0)==0 and hs.count(0)==0:
    break
    
for player in range(0, no_players):
  print('Player', player+1, 'has won', our_completed_squares[player], 'squares', end=' ')
  
  if max(no_completed_squares) == our_completed_squares[player]:
    print('And so is a (potentially) joint winner!)
  
  else:
    print() 
```

The first `if` statement is part of the `turn` loop yet references the end of the game so we mention it here. It breaks out of that loop if all lines have been drawn in.

Finally, the program prints out the scores of all players in the game, and prints a message if they are a winner.

## Piggy.py

## 2x2 Minimax.py

The brute force minimax algorithm for a 2x2 game of Dots and Boxes shall pivot around the game tree of the game, that is, a list of all possible states that the game could be in. It is initialised as follows:

```Python
game_tree=[[], [[[], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], 1, 0, 0, -1], [[], [0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], 1, 0, 0, -1]]]
```

This is a 3D Array that, here, stores the game states that are 'first horizontal filled in' and 'second vertical filled in'. In fact, these are the only first two moves of the game because of the many symmetries of the 2x2 grid. The many different components of each game state are described as follows:

```Python
## game_tree[depth_index][leaf_index][0] is list of the leaf_index of the leaf's parents
## game_tree[depth_index][leaf_index][1] are the horizontals (list) 
## game_tree[depth_index][leaf_index][2] are the verticals (list) 
## game_tree[depth_index][leaf_index][3] next players turn
## game_tree[depth_index][leaf_index][4] is player 0's no. squares won
## game_tree[depth_index][leaf_index][5] is player 1's no. squares won
## game_tree[depth_index][leaf_index][6] player who has won (-1 if still open game)
```

This extended comment was kept in this program as I developed it since it was an extremely useful reference that allowed for the code to be vastly shortened yet still easy to write.

```Python
for depth in range(2, 13):
    game_tree.append([]) ## the new depth level

    for index in range(0, len(game_tree[depth-1])): ## for leaf in previous level

        current_leaf=game_tree[depth-1][index] ## eek
```

These are the first lines of the loop of the body of the program. They iterate through `depth`s which are the sub-lists of every game state with `depth` number of moves made, and then iterate through each move in the previous depth so that the future moves build off of these moves. 

``` Python
for horizontal in range(0, 6):
        if current_leaf[1][horizontal]==0:
               new_leaf=current_leaf ## this doesn't behave properly
```

This was the initial code that I used to make each new move that could be made from the stem game state. However, the behaviour of Python with regard to intialising lists I found to be unsuitable for my needs, as all changes that were later made to `new_leaf` were also made to `current_leaf`, which, for example caused all moves to be superimposed onto `current_leaf` in the second depth, and the program to thus crash. This prompted the definition of the function

```Python
def deep_copy(lis):
    new_lis=[]
    for elem in lis:
        if type(elem)==list:
            new_lis.append(deep_copy(elem))
        else:
            new_lis.append(elem)
    return new_lis
```

Called `deep_copy` because of the nature of the function, to not 'surface copy' lists and cause errors as above. Indeed, the code three segements above was changed to 

``` Python
for depth in range(2, 13):
    game_tree.append([]) ## the new depth level

    for index in range(0, len(game_tree[depth-1])): ## for leaf in previous level

        current_leaf=deep_copy(game_tree[depth-1][index]) ## has become deep_copy
```

and the code two segements above

``` Python
for horizontal in range(0, 6):
        if current_leaf[1][horizontal]==0:
               new_leaf=deep_copy(current_leaf) ## now deep_copy
```

The next segement of the code manipulates `new_leaf` to update the number of squares won in this game state, whose turn it is, and finally if the game has been won.

``` Python
                new_leaf[0]=[index] ## this is the parent branch
                
                new_leaf[1][horizontal]=1

                squares_difference=completed_squares(new_leaf[2], new_leaf[1])-completed_squares(current_leaf[2], current_leaf[1])

                if squares_difference>0: ## if squares have been won, we need to know about it
                    new_leaf[4+new_leaf[3]]+=squares_difference

                    if new_leaf[4] > 2: new_leaf[6]=0
                    if new_leaf[5] > 2: new_leaf[6]=1

                else: ## change turn. this means that what we're measuring is *next* turn
                    new_leaf[3]=(new_leaf[3]+1)%2
```

It is here where the comments on what exactly `new_leaf[2]` was doing were immensely useful. Note that the function `completed_squares` has been copied over to this program from the previous two programs. The final element of the main body of the program is the control sequence

```Python
                if isin(game_tree[-1], new_leaf)==-1:
                    game_tree[-1].append(new_leaf)

                else:
                    new_index=isin(game_tree[-1], new_leaf)
                    game_tree[-1][new_index][0].append(index)
```

that was changed from an earlier iteration of the program in order to drastically increase the efficiency of the program. See the main essay for commentary on this stage, as its illustration of the power of optimisation was an important talking point in my essay.

What this block of code is doing is making sure that game states are not added twice to the `game_tree`. This is often an important step in Breadth First Search (BFS) algorithms. Once again, see the essay.

The function `is_in` is fairly simple ...

## General Solution.py

The final program in this repository and my project as a whole is the general Dots and Boxes AI player. Again, this program shall use the minimax algorithm in order to make its moves, yet whereas in `2x2 Minimax.py` the minimax algorithm used finished games to backtrack, this program shall use Berlekamp's 'chain rule' (see accompanying essay) in order to reach game states from which it will win.

However, the chain rule is not enough on its own to make an AI player, as after the critical state where the right number of chains are obtained, the AI player will still need to take squares from such chains. Thus there are two parts to the implementation of this final program.

The first function that will need to be implemented here is the function `is_critical` that determines whether the game is in a critical state, i.e any move will cause a sacrifice. We reimplement (with, as above, some modifications in order to ensure that this function works on any size grid, not simply square grids) the function ```is_winnable_square``` from the ```Piggy.py``` program, in order to determine whether each move that we make on the current board could lead to the opponent taking a square:

```Python
def is_critical(hs, vs, rs, cs): ## try to find a non critical

        ## assuming we can't ALREADY TAKE a square

        for horizontal in range(0, (rs+1)*cs):

                if hs[horizontal] == 0:

                        newh = hs[:]

                        newh[horizontal] = 1

                        if is_winnable_square(newh, vs, rs, cs) == False:

                                return False

        for vertical in range(0, (cs+1)*rs):

                if vs[vertical] == 0:

                        newv = vs[:]

                        newv[vertical] = 1

                        if is_winnable_square(hs, newv, rs, cs) == False:

                                return False

        return True
```

The basic control flow of the game of Dots-and-Boxes is little changed from that in the `Simulator.py` or `Piggy.py`:

```
for turn in count():

        move_made = False

        if players_turn == 0:

        ## players turn

                move_made = input('It\'s your move, player! >')

        else: ## AI turn

                if f(rows*columns + rows + columns) // f(rows*columns) < 10**8: ## is this a good bound ?!

                        ## we can minimax for critical state, check for parity of chains

                        pass

                else:

                        if is_winnable_square(hs, vs, rs, cs)!=False: ## we can take a square!! 

                                move_made=is_winnable_square(hs, vs, rs, cs)
                             
                        ## take a square if it's there

                        ## don't sacrifice otherwise

                        pass

        completed = completed_squares(vs, hs, rows, columns) ## prior completed squares

        if move_made[0] == 'h':

                hs[int(move_made[1:])] = 1

        if move_made[1] == 'v':

                vs[int(move_made[1:])] = 1

        if completed_squares(hs, vs, rows, columns) > completed: ## rotate turn

                our_completed_squares[players_turn] += completed_squares(hs, vs, rows, columns)-completed

        else: ## rotate turn

                players_turn+=1
                players_turn=players_turn%2
```

