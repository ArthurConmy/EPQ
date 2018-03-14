from itertools import count

##colours!

white='\033[1;37m'
black='\033[1;30m'
reset='\033[0m'

## print('{}ofwgkta{}'.format(white, reset)) colour test

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
                
def completed_squares(verticals, horizontals, bs):

    the_completed_squares=[]
    
    for upper in range(0, len(horizontals)-bs): 
        if horizontals[upper]==1: 
            if horizontals[upper+bs]==1:
                if verticals[upper + upper//bs]==1: 
                    if verticals[upper + upper//bs + 1]==1:
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

board_size=4

hs=[0 for i in range(0, board_size*(board_size+1))]
vs=[0 for i in range(0, board_size*(board_size+1))]

no_players=2

our_completed_squares=[0 for i in range(0, no_players)]

players_turn=0

for turn in count(1):
  
  print_game(vs, hs, board_size)
  
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
    
  if vs.count(0)==0 and hs.count(0)==0:
    break
    
for player in range(0, no_players):
  print('Player', player+1, 'has won', our_completed_squares[player], 'squares', end=' ')
  
  if max(no_completed_squares) == our_completed_squares[player]:
    print('And so is a (potentially) joint winner!')
  
  else:
    print()

