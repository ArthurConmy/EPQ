from random import randint

##colours!

white='\033[1;37m'
black='\033[1;30m'
reset='\033[0m' ## turn these colours on on repl.it. Not in IDLE tho

def print_game(horizontals, verticals, rs, cs): ##if you're in repl.it, turn this into print_game and delete the function below
  
    for index in range(0, rs+1):
        for index_2 in range(index*cs, (index+1)*cs):
            if horizontals[index_2]==1:
                print('{} --'.format(white), end='')
            else:
                print('{} --{}'.format(black, reset), end='') ## colour ?!
        print()
        if index!=rs:
            for index_3 in range(index*(cs+1), (index+1)*(cs+1)):
                if verticals[index_3]==1:
                    print('{}|  {}'.format(white, reset), end='')
                else:
                    print('{}|  {}'.format(black, reset), end='')
        print()
                
def completed_squares(hs, vs, rs, cs): ## Returns the number of completed squares (all players)

    the_completed_squares=0 ##=[]
    
    for upper in range(0, rs*cs): ## dependent on board_size !!!
        if hs[upper]==1 and hs[upper+cs]==1 and vs[upper + upper//cs]==1 and vs[upper + upper//cs + 1]==1:
            the_completed_squares+=1 ##.append(upper)
                
    return the_completed_squares ## used to be len

def is_winnable_square(hs, vs, rs, cs):
  
        ##print(hs)
        ##print(vs)

        for horizontal in range(0, rs*cs):
          
                ##print(horizontal, horizontal + cs, horizontal + horizontal//cs, horizontal + horizontal//cs + 1)

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
                        return move

        else:
                return False
                
def no_consecutive_takeable_squares(hs, vs, rs, cs): ## take as many squares as possible!

    copyh = hs[:]
    copyv = vs[:]

    number = 0

    while is_winnable_square(copyh, copyv, rs, cs) != False:

        number+=1

        move_made = is_winnable_square(copyh, copyv, rs, cs)
        #print(move_made)

        if move_made[0] == 'h':

                copyh[int(move_made[1:])] = 1
                #print('changed')

        if move_made[0] == 'v':

                copyv[int(move_made[1:])] = 1
                #print('changed too')

    return number
  
def random_from_list(lis):
  return lis[randint(0, len(lis)-1)]
      
rows=3
columns=4

hs=[0 for i in range(0, (rows+1)*columns)]
vs=[0 for i in range(0, (columns+1)*rows)]

no_players=2

our_completed_squares=[0 for i in range(0, no_players)]

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

    if completed_squares(hs, vs, rows, columns) > sum(our_completed_squares):
      print('Player', players_turn+1, 'takes', completed_squares(hs, vs, rows, columns)-sum(our_completed_squares), 'square(s)! They get another go!')
      our_completed_squares[players_turn]+=completed_squares(hs, vs, rows, columns)-sum(our_completed_squares)
  
    else:
      players_turn+=1
      players_turn=players_turn%2
      
  else: ## It's the computer's turn

    print('The computer\'s turn')
    
    ## if can_square_be_taken==True:
    
    if is_winnable_square(hs, vs, rows, columns) != False:
      move_made=is_winnable_square(hs, vs, rows, columns)
    
    ## elif can_square_not_be_given_away==True:
    
    else: 
      
      candidate_moves=[]
      
      for horizontal in range(0, columns*(rows+1)):
        if hs[horizontal]!=1:
          copyh=list(hs)
          copyh[horizontal]=1 
          if is_winnable_square(copyh, vs, rows, columns)==False:
            candidate_moves.append('h'+str(horizontal))

      for vertical in range(0, rows*(columns+1)):
        if vs[vertical]!=1:
          copyv=list(vs)
          copyv[vertical]=1 
          if is_winnable_square(hs, copyv, rows, columns)==False:
            candidate_moves.append('v'+str(vertical))
      
      if len(candidate_moves)>0:
        move_made=random_from_list(candidate_moves)
        
      else: ## we have to sacrifice. This is done at random but could be done FAR better
        moves=[]
        
        for horizontal in range(0, columns*(rows+1)):
          if hs[horizontal]==0:
            moves.append('h'+str(horizontal))
        for vertical in range(0, rows*(columns+1)):
          if vs[vertical]==0:
            moves.append('v'+str(vertical))
        
        move_made=random_from_list(moves)
      
    ## else for move in moves
    
    move_made=[move_made[0], int(move_made[1:])]
    if move_made[0]=='h':
      hs[move_made[1]]=1
    
    if move_made[0]=='v':
      vs[move_made[1]]=1

    if completed_squares(hs, vs, rows, columns) > sum(our_completed_squares):
      print('Player', players_turn+1, 'takes', completed_squares(hs, vs, rows, columns)-sum(our_completed_squares), 'square(s)! They get another go!')
      our_completed_squares[players_turn]+=completed_squares(hs, vs, rows, columns)-sum(our_completed_squares)
  
    else:
      players_turn+=1
      players_turn=players_turn%2
      
  print_game(hs, vs, rows, columns)

if our_completed_squares[0]>our_completed_squares[1]:
  print('You win!')
  
else:
  
  if our_completed_squares[0]<our_completed_squares[1]:
    print('Computer wins')
    
  else:
    print('Draw')
