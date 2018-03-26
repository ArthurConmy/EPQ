# EPQ

This repository holds all important files in the EPQ qualification I am working towards.

The following ReadMe also documents the research and development in my project, from its conception towards the final program which I tested against myself.

To play against my artefact, visit https://repl.it/@HuskerDu/EPQ-General-Solution and click the 'run' button.

# Initial Aims, Research

My aims are as follows:

* To develop a working computer opponent to the Dots-and-Boxes game
* To improve the 'working' computer opponent such that it is at the ability of an intermediate ability human player
* To test the computer opponent against myself, to be able to quantify the above aim

Note that these have been developed from the more general and background research that I have already carried out; see the accompanying essay to this project. My research, however, is ongoing and thus this report, too, is referenced where external sources have influenced decision making.

In order to meet the above aims, I shall do the following:

Use the Python programming language in order to develop in the following order:

* A simulator that allows any number of players to play a game of Dots-and-Boxes on an arbitrarily-sized grid
* A simple greedy algorithm opponent 
* A more complicated (minimax algorithm based) opponent, that only plays Dots-and-Boxes games on smaller grids
* A general minimax opponent

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/python-logo.png" width="200" height="100"/> |
|:--:| 
| *The Python Logo* |

There are several decisions made here that need to be expounded and/or justified.

To begin, the choice of Python as the programming language. This was made for two reasons: first, this is the language that I am most familiar with, and secondly, because it is one of the most intuitive languages to read and thus debug [1]. I plan to use the IDLE 
IDE in order to code my program, which has many features that will be helpful to my project, such as auto-coloured text allowing easy distinguishing between functions, variables and loops [2].

The progression from greedy to minimax algorithm is justified from personal experience and intiution, and by their very defintion [3] greedy algorithms have the inbuilt susceptibility to be weak to more advanced strategies. Being a complex and much-studied game, Dots-and-Boxes is not likely to be a game which a greedy algorithm is effective at playing. On the other hand, minimax algorithms are at the heart of many competitive computer programs [4] for Chess and Draughts, for example.

I began the development of my artefact with the aforementioned simulator program. It's development is described below.

# Simulator.py

The first section of `Simulator.py` is

```Python
board_size=4

hs=[0 for i in range(0, board_size*(board_size+1))]
vs=[0 for i in range(0, board_size*(board_size+1))]

no_players=2

our_completed_squares=[0 for i in range(0, no_players)]

players_turn=0
```

These 10 lines of code are the initialisation of a Dots-and-Boxes game. The variables defined are `board_size`, `hs`, `vs`, `no_players`, `our_completed_squares` and `players_turn`. Several are self-explanatory, but `hs` and `vs` are lists that store boolean values for whether each horizontal and vertical has been filled in. The reason for their abbreviated identifiers is their prevalence in the code, which means that it will be easier to code the rest of the program since typing will be faster.

The looping structure for the program is not particularly complex: it is essentially a `while True:` loop, but not exactly this since we would like to be able to know which turn of the game it is. Instead

```Python

from itertools import count 

## ... things

for turn in count(1):

  ## each turn of the game
```

creates a variable `turn` that is the turn of the game for which a move is being made. This of course uses the `count` iterator from the  `itertools` library.

The first piece of code inside this `for` loop is

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

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/bad%20interface.png" width="300" height="400"/> |
|:--:| 
| *Note the awkward, 'floating' lines in the grid* |

At this stage, after a conversation with a friend who I had just played a game against, I decided that this interface was inadequate for the purposes of my Dots-and-Boxes simulator, and thus the future programs too.

Instead, the following redefinition of `print_game` allows for the lines in the grid yet to be filled in to be coloured in a much darker shade, yet their presence is still definite.

``` Python
white='\033[1;37m'
black='\033[1;30m'
reset='\033[0m'

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

I found such example codes on the website `repl.it` [5]. In fact, in finding the colours available more readily in `repl.it`, and the fact that programs are given a URL immediately, `repl.it` was attractive as an IDE. 

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/replitinterface.png" height="400"/> |
|:--:| 
| *The new interface in `repl.it`. The grid in the background provides a much better Dots-and-Boxes playing experience* |

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

# Piggy.py

It is now time to develop a computer opponent to the Dots and Boxes game, this following an aforementioned 'greedy algorithm' (from [3], 'an algorithm that always takes the best immediate, or local, solution while finding an answer), which in this context will greedily take a square whenever it can, and otherwise sacrifices as few squares as possible. I developed a flow chart to stay focused on such an algorithm:

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/drawio.png" height="400"/> |
|:--:| 
| *The flow chart documenting the control flow of the greedy algorithm* |

... (Improvements section? After all, the original code was the stuff that was tested against Ruth)

Originally, the following piece of code was used to make a move if there were no squares available to be taken and no neutral squares either

``` Python
      else: ## we have to sacrifice. This is done at random but could be done FAR better
        moves=[]
        
        for horizontal in range(0, columns*(rows+1)):
          if hs[horizontal]==0:
            moves.append('h'+str(horizontal))
        for vertical in range(0, rows*(columns+1)):
          if vs[vertical]==0:
            moves.append('v'+str(vertical))
        
        move_made=random_from_list(moves)
```

However, this was quickly found to be inadequate, as the nature of Dots-and-Boxes is such that many chains are available to be taken at the end of the game, and that in fact a random move is much more likely to make a large sacrifice of boxes than a small number. Instead, the following code sacrifices the least number of possible squares that it can;

``` Python
else:
        moves=[]
        min_takable = rows*columns # worse case scenario we have to take EVERY square
        
        for horizontal in range(0, columns*(rows+1)):
          
          if hs[horizontal]==1: continue
        
          copyh=hs[:]
          copyh[horizontal]=1 
          
          takey = no_consecutive_takeable_squares(copyh, vs, rows, columns)
          
          if takey > min_takable: continue
        
          if takey == min_takable:
            moves.append('h'+str(horizontal))
            
          else: # takey < min_takable  
            min_takable=takey
            moves=['h'+str(horizontal)]
            
        for vertical in range(0, rows*(columns+1)):
          
          if vs[vertical]==1: continue
        
          copyv=vs[:]
          copyv[vertical]=1 
          
          takey = no_consecutive_takeable_squares(hs, copyv, rows, columns)
          
          if takey > min_takable: continue
        
          if takey == min_takable:
            moves.append('v'+str(vertical))
            
          else: # takey < min_takable  
            min_takable=takey
            moves=['v'+str(vertical)]
            
        move_made=random_from_list(moves)
```

Characteristic of much of the progress in this project, what seems like a trivial improvement requires a significant chunk of code, 40 lines in this case! However, such an improvement is very important for the development of a reasonable greedy algorithm that will challenge novice players of Dots-and-Boxes.

## 2x2 Minimax.py

We now moved on to the much cleverer approach to the Dots-and-Boxes opponent; the minimax algorithm. However, the difficulty of programming a minimax algorithm being much greater than the difficulty of programming a greedy algorithm, we decided to code a minimax algorithm not for arbitrarily sized Dots-and-Boxes grids, but only for a 2x2 grid. Furthermore, this program would have an 'evaluator function' (see accompanying essay) as the game being won, as opposed to a more short term evaluator.

The brute force minimax algorithm for a 2x2 game of Dots and Boxes pivoted around the game tree of the game, that is, a list of all possible states that the game could be in. It is initialised as follows:

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

The function `is_in` is fairly simple, allowing us to determine whether we've already encountered a leaf prior in the minimax search, as we parse all the leafs we encounter through this function to make sure that they are not double up:

``` Python
def isin(big, small):
    for thing in big:
        if thing[1:]==small[1:]:
            return big.index(thing)
    return -1
```

We return `-1` in this function rather than `False` because of ambiguities with the behaviour of the `big.index(thing)` which on occasion returned `0` which is synonomous with `False` in Python [6]. 

After the BFS was completed, the minimax search was initialised; it was not particularly difficult to:

```Python
for depth in range(12, 1, -1):

    for leaf in game_tree[depth]:

        if leaf[6]!=-1:

            if leaf[3] == leaf[6]: ## the player who has won is the same as the player who has just made the move

                for index in leaf[0]:

                    game_tree[depth-1][index][6] = leaf[3]
```

this code simply making each leaf backtrack where possible.

The rest of this program simply borrows from `Greedy.py`; pitting a human player against the minimax opponent. This was in fact underwhelming; see the essay.

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

The basic control flow of the game of Dots-and-Boxes is little changed from that in the `Simulator.py` or `Piggy.py`. The computer player's control flow is documented in commented-out pseudocode in order to guide the programming of this crucial section.

``` Python
for turn in count():

        move_made = False

        if players_turn == 0:

        ## players turn

                move_made = input('It\'s your move, player! >')

        else: ## AI turn

                if is_winnable_square(vs, hs, rows, columns)!=False:

                        ## if neutral squares left
                        ## then take square

                        ## else if squares in long chain
                        ## then take all but last two

                        ## else take square

                        pass

                else: ## no winnable squares

                        ## if can play neutral move
                        ## then minimax to try to reach right parity of chains

                        ## else sacrifice the least valuable chain, attempting to not let the sacrifice be returned

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

The pseudocode above once more requires the definition of several more functions, including ```is_neutral_square``` to return a boolean value whether there is a move that can be made that will not cause the opponenent to be able to take any squares. This function in turn requires the definition of the function ```no_winnable_squares``` that returns the number of winnable squares on the board.

However, before implementing such functions I took a step back to reevaulate a certain aspect of the aims of my project, this being the decision to use IDLE as the IDE for my program. The sheer number of functions already defined in `General Solution.py` made navigating the program difficult, so approaching a critical stage where even more functions needed to be defined, I transferred my project to the Visual Studio program, which provides the very useful minimisation tool for functions to make code compact and readable, and in addition to this has adjustable zoom on the mouse which allows for quick naviagtion of the code.

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/vslogo.png" width="100" height="100"/> |
|:--:| 
| *Microsoft Visual Studio* |

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/c1d81fcbfaa34f751e73924e7bf5743d.gif" width="400" height="400"/> |
|:--:| 
| *Minimising a function. Blink and you'll miss it!* |

| <img src="https://github.com/ArthurConmy/EPQ/blob/images/7590d0a015e6b50134b384bba53e0370.gif" width="400" height="400"/> |
|:--:| 
| *Zooming in to a function* |

```Python
def no_winnable_squares(hs, vs, rs, cs):

        no=0

        for horizontal in range(0, rs*cs):

                no_filled = 0

                if hs[horizontal] == 1:
                        no_filled+=1
                else:
                        move = 'h'+str(horizontal)

                if hs[horizontal + cs] == 1:
                        no_filled+=1
                else:
                        move = 'h'+str(horizontal + cs)

                if vs[horizontal + horizontal//cs] == 1:
                        no_filled+=1
                else:
                        move = 'v'+str(horizontal + horizontal//cs)

                if vs[horizontal + horizontal//cs + 1] == 1:
                        no_filled+=1
                else:
                        move = 'v'+str(horizontal + horizontal//cs + 1)

                if no_filled == 3:
                        no+=1

        return no

def is_neutral_square(hs, vs, rs, cs): ## is there a neutral move that can be made ?

        no_winnable = no_winnable_squares(hs, vs, rs, cs)

        for h in range(0, rs*cs):

                if hs[h] == 1: continue
                
                copyh=hs[:]
                copyh[h]=1

                if no_winnable_squares(copyh, vs, rs, cs) == no_winnable: return True ## ie theres a move that doesn't change the number of winnable squares
                
        for v in range(0, rs*cs):

                if vs[v] == 1: continue

                copyv=vs[:]
                copyv[v]=1

                if no_winnable_squares(hs, copyv, rs, cs) == no_winnable: return True

        return False
```

Such functions allowed the general solution to be able written compactly. In fact there are even more such functions defined in `General Solution.py`: these being

```Python
def no_neutrals(hs, vs, rs, cs):
  ...
  
def no_consecutive_takeable_squares(hs, vs, rs, cs):
  ...
  
def parity_long_chains(hs, vs, rs, cs):
  ...
```

The first two being self-explanatory; `no_neutrals` returning the number of consecutive neutral moves that can be made on a given grid, and `no_consecutive_takeable_squares` returning the number of squares that can be taken consecutively on a given grid. `parity_long_chains` returns the parity (`0` being even, `1` being odd) of the number of so called 'long chains' in a given Dots-and-Boxes grid.

The importance of these functions lies in the minimax search; see the accompanying essay for explanation of Berlekamp's 'long chain rule' which is central to our minimax search. In particular, lines of code such as 

``` Python 
                          if no_neutrals(hs, vs, rows, columns) <= max_ply:
                            
                              print('Beginning minimax')
                              print('Please wait ...')
```
show the initialisation of the minimax search, in particularly intuitive manner. that is, `no_neutrals(hs, vs, rows, columns)` provides a reasonable estimate for the ply depth of the minimax, and the `if` statement compares such an estimate to the user inputted `max_ply` variable, which sets out the maximum ply that the program is permitted to such to.

Within the above `if` clause,

# Expert Feedback

Wanting some expert advice on my program, I got into contact with a computing teacher at my school, Dr Peter Panagi, who was to advise me on the code that I had produced. His advice, which were often prompted by my concerns, fell into the two following categories

* Interface
* Classes

With regard to the interface of my program, Dr Panagi instantly was disconcerted by the lack of instructions for how to enter moves. This was something that I had failed to implement solely because of my own familiarity with such move entry, but I realised seeing him play the game that it was not intuitive that 'hN' entered the Nth horizontal move, for example. This was to be a fairly brief improvement to my program and Dr Panagi understood the reason why it had been omitted, yet stressed the importance of software being designed constantly with the consumer in mind.

On the other hand Dr Panagi appreciated much of the rest of the interface of my program - this included the winner/loser messages printed at the end of the game and the skill level of the computer player.

In terms of classes, these had been something I had been concerned with throughout my project; I considered myself a competent Python programmer yet did not know how to implement classes in Python, and thus was worried that my code was substandard due to this. However Dr Panagi reassured me that classes were not necessary within my program, nor was my program significantly disadvantaged because of their absence. He emphasised the fact that my code *worked*, in addition to the fact that my use of functions and whitespace within the code showed clearly that I had planned and organised my code with a lot of care and thought, and that classes would have made only a trivial difference to my project.

Responding quickly to the expert feedback, I added instructions to my program. These surrounded the preexistent prompts for the player to enter the number of rows, columns and maximum ply.

```Python
print('Welcome to the general solution Dots-and-Boxes opponent!')
print()

print('First, you will have to enter the number of rows, columns and the maximum ply for the minimax search. Do so now:')
print()
  
rows = int(input('Enter number of rows >'))
columns = int(input('Enter number of columns >'))
max_ply = int(input('Enter maximum ply for the minimax search. 8 will be slow, 6 medium, 4 fast >'))
print()

print('To enter a horizontal move, enter \'hN\' (without the quotation marks) in order to enter the Nth horizontal move, which is counted from 0. Thus \'h0\' is the first horizontal move, and likewise \'v0\' is the first vertical move.')
print()
print('It may be best to play a couple of practise games with this program before a \'serious\' game, to become accustomed to this method of entering moves')
print()
print('We\'re about to begin: a blank grid shall be printed, which shall have white lines drawn onto after moves have been made. Good luck!')
print()
```

# References

* [1], from https://www.python.org/about/: 'Python is powerful... and fast; 
plays well with others; 
runs everywhere; 
**is friendly & easy to learn;** 
is Open. Accessed 21/03/2018

* [2], a complete list of the features of IDLE can be found at: https://docs.python.org/3/library/idle.html. Accessed 21/03/2018

* [3], National Institute of Standards and Technology: 'Greedy Algorithm': https://xlinux.nist.gov/dads//HTML/greedyalgo.html. Accessed 21/03/2018

* [4], Stanford University, 'Deep Blue': *'... first put forth the idea of **a function for evaluating the efficacy of a particular move and a "minimax" algorithm which took advantage of this evaluation function** by taking into account the efficacy of future moves that would be made available by any particular move. This work provided a framework for all future research in computer chess playing.'* http://stanford.edu/~cpiech/cs221/apps/deepBlue.html. Accessed 21/03/18

* [5], 'Colored Text!' by @rocco, https://repl.it/@rocco/Coloured-Text. Accessed 20/02/18. 404 not found on 21/03/18; luckily I had forked the project to https://repl.it/@HuskerDu/Coloured-Text. Accessed 21/03/18.

* [6] Python Enhancement Protocol no. 285: 'Adding a bool type' https://www.python.org/dev/peps/pep-0285/. Accessed 21/03/18
