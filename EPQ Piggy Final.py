from random import randint

##colours!

white='\033[1;37m'
black='\033[1;30m'
reset='\033[0m' ## turn these colours on on repl.it. Not in IDLE tho tho

## print('{}ofwgkta{}'.format(white, reset)) colour test

def repl_print_game(verticals, horizontals, bs): ##if you're in repl.it, turn this into print_game and delete the function below
  
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
        
def print_game(verticals, horizontals, bs): ## Takes input as the horizontals and verticals of the game. Prints the board. Doesn't account for drawing letters in squares that have been won
  
    for index in range(0, bs+1):
        for index_2 in range(index*bs, index*bs + bs):
            if horizontals[index_2]==1:
                print(' --', end='')
            else:
                print('   ', end='')
        print()
        if index!=bs:
            for index_3 in range(index*(bs+1), index*(bs+1) + bs + 1):
                if verticals[index_3]==1:
                    print('|  '.format(white, reset), end='')
                else:
                    print('   '.format(black, reset), end='')
        print()
                
def completed_squares(verticals, horizontals, bs): ## Returns the number of completed squares (all players)

    the_completed_squares=[]
    
    for upper in range(0, len(horizontals)-bs): ## dependent on board_size !!!
        if horizontals[upper]==1 and horizontals[upper+bs]==1 and verticals[upper + upper//bs]==1 and verticals[upper + upper//bs + 1]==1:
            the_completed_squares.append(upper)
                
    return len(the_completed_squares)

def is_winnable_square(verticals, horizontals, board_size):
  
  for horizontal in range(0, board_size**2):
    filled=0
    spare=-1
    if horizontals[horizontal]==1:
      filled+=1
    else:
      spare='h'+str(horizontal)
    if horizontals[horizontal+board_size]==1:
      filled+=1
    else:
      spare='h'+str(horizontal+board_size)
    if verticals[horizontal + horizontal//board_size]==1:
      filled+=1
    else:
      spare='v'+str(horizontal + horizontal//board_size)
    if verticals[horizontal + horizontal//board_size + 1]==1:
      filled+=1 
    else:
      spare='v'+str(horizontal + horizontal//board_size + 1)
    if filled==3:
      return spare
  
  return False
  
def random_from_list(lis):
  return lis[randint(0, len(lis)-1)]
      
board_size=3

hs=[]
vs=[] ## horizontals and verticals of the board have been initialised

for i in range(0, board_size*(board_size+1)):
    hs.append(0)
    vs.append(0)

no_players=2

our_completed_squares=[]

for do_this in range(0, no_players):
  our_completed_squares.append(0)

players_turn=0 ## player 1 is 0, and player 2 is 1. Also this starts at 1 so the loop can begin with the increment

while hs.count(0)+vs.count(0)>0:
  
  if players_turn==0: ## Let's say player 0 is the human player. It's their turn
    move_made=input('Player '+str(players_turn+1)+' Enter your move')
    move_made=[move_made[0], int(move_made[1:])]
  
  ## intercept invalid moves. including 'double' moves
  
    if move_made[0]=='h':
      hs[move_made[1]]=1
    
    if move_made[0]=='v':
      vs[move_made[1]]=1

    if completed_squares(vs, hs, board_size) > sum(our_completed_squares):
      print('Player', players_turn+1, 'takes', completed_squares(vs, hs, board_size)-sum(our_completed_squares), 'square(s)! They get another go!')
      our_completed_squares[players_turn]+=completed_squares(vs, hs, board_size)-sum(our_completed_squares)
  
    else:
      players_turn+=1
      players_turn=players_turn%2
      
  else: ## It's the computer's turn

    print('The computer\'s turn')
    
    ## if can_square_be_taken==True:
    
    if is_winnable_square(vs, hs, board_size)!=False:
      move_made=is_winnable_square(vs, hs, board_size)
    
    ## elif can_square_not_be_given_away==True:
    
    else: ##Not sure if this is working. Some kind of bug where a move stays locked ... ?
      candidate_moves=[]
      
      for horizontal in range(0, board_size*(board_size+1)):
        if hs[horizontal]!=1:
          copyh=list(hs)
          copyh[horizontal]=1 
          if is_winnable_square(vs, copyh, board_size)==False:
            candidate_moves.append('h'+str(horizontal))

      for vertical in range(0, board_size*(board_size+1)):
        if vs[vertical]!=1:
          copyv=list(vs)
          copyv[vertical]=1 
          if is_winnable_square(copyv, hs, board_size)==False:
            candidate_moves.append('v'+str(vertical))
      
      if len(candidate_moves)>0:
        move_made=random_from_list(candidate_moves)
        
      else: ## we have to sacrifice. This is done at random but could be done FAR better
        moves=[]
        for horizontal in range(0, board_size*(board_size+1)):
          if hs[horizontal]==0:
            moves.append('h'+str(horizontal))
        for vertical in range(0, board_size*(board_size+1)):
          if vs[vertical]==0:
            moves.append('v'+str(vertical))
        move_made=random_from_list(moves)
      
    ## else for move in moves
    
    move_made=[move_made[0], int(move_made[1:])]
    if move_made[0]=='h':
      hs[move_made[1]]=1
    
    if move_made[0]=='v':
      vs[move_made[1]]=1

    if completed_squares(vs, hs, board_size) > sum(our_completed_squares):
      print('Player', players_turn+1, 'takes', completed_squares(vs, hs, board_size)-sum(our_completed_squares), 'square(s)! They get another go!')
      our_completed_squares[players_turn]+=completed_squares(vs, hs, board_size)-sum(our_completed_squares)
  
    else:
      players_turn+=1
      players_turn=players_turn%2
      
      
  print_game(vs, hs, board_size)

if our_completed_squares[0]>our_completed_squares[1]:
  print('You win!')
  
else:
  if our_completed_squares[0]<our_completed_squares[1]:
    print('Computer wins')
    
  else:
    print('Draw')
