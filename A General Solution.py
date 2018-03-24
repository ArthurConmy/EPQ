from itertools import count
from math import factorial as f
from random import randint

white='\033[1;37m'
black='\033[1;30m'
reset='\033[0m'

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

def is_critical(hs, vs, rs, cs): ## try to find a non critical

        ## assuming we can't ALREADY TAKE a square

        for horizontal in range(0, (rs+1)*cs):

                if hs[horizontal] == 0:

                        newh = hs[:]

                        newh[horizontal] = 1

                        if is_winnable_square(newh, vs, rs, cs) == False:

                                return 'h'+str(horizontal)

        for vertical in range(0, (cs+1)*rs):

                if vs[vertical] == 0:

                        newv = vs[:]

                        newv[vertical] = 1

                        if is_winnable_square(hs, newv, rs, cs) == False:

                                return 'v'+str(vertical)
        return True

def is_winnable_square(hs, vs, rs, cs):

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
                        return move

        else:
                return False

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

        for h in range(0, (rs+1)*cs):

                if hs[h] == 1: continue
                
                copyh=hs[:]
                copyh[h]=1

                if no_winnable_squares(copyh, vs, rs, cs) == no_winnable: return True ## ie theres a move that doesn't change the number of winnable squares
                
        for v in range(0, rs*(cs+1)):

                if vs[v] == 1: continue

                copyv=vs[:]
                copyv[v]=1

                if no_winnable_squares(hs, copyv, rs, cs) == no_winnable: return True

        return False

def no_neutrals(hs, vs, rs, cs): ## how many (naively) neutral moves from this point?

  number=0
  
  copyh=hs[:]
  copyv=vs[:]
  
  while is_critical(copyh, copyv, rs, cs)!=True:
    
    number+=1
    
    move=is_critical(copyh, copyv, rs, cs)
    
    if move[0]=='h':
      copyh[int(move[1:])]=1
      
    else:
      copyv[int(move[1:])]=1
      
  return number

def completed_squares(hs, vs, rs, cs): ## Returns the number of completed squares (all players)

    the_completed_squares=0 ##=[]
    
    for upper in range(0, rs*cs): ## dependent on board_size !!!
        if hs[upper]==1 and hs[upper+cs]==1 and vs[upper + upper//cs]==1 and vs[upper + upper//cs + 1]==1:
            the_completed_squares+=1 ##.append(upper)
                
    return the_completed_squares ## used to be len

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

rows = 3 
columns = 3

hs=[0 for i in range(0, columns*(rows+1))]
vs=[0 for i in range(0, rows*(columns+1))]

no_players=2

our_completed_squares=[0 for i in range(0, no_players)]

players_turn=0

critical_yet = False

for turn in count():
  
        print(hs)
        print(vs)
  
        print()
        print_game(hs, vs, rows, columns)

        if hs.count(0)+vs.count(0)==0: break ## game over

        move_made = False

        if players_turn == 0: ## players turn

                move_made = input('It\'s your move, player! >')

        else: ## AI turn

                if is_winnable_square(hs, vs, rows, columns)!=False:

                        ## if neutral squares left
                        ## then take square

                        if no_neutrals(hs, vs, rows, columns)>1:

                                move_made = is_winnable_square(hs, vs, rows, columns)
                                print('Making move thats taking a square because neutral squareS exist')

                        ## else if squares in long chain
                        ## then take all but last two

                        ## okay several functions to be defined here
                        ## one function that takes as many squares as it can, so we know how many squares are winnable
                        ## another that lists all moves that are part of 

                        else: ## NO neutral squares

                            if no_consecutive_takeable_squares(hs, vs, rows, columns)>2: ## multiple takeable squares

                                move_made = is_winnable_square(hs, vs, rows, columns)
                                print('More than 2 winnable squares so getting the winnable square')

                            else: ## no_consecutive_takeable_squares is EQUAL to 2.

                                ##try and make move that doesn't cause completed squares to increase

                                is_move_made = False

                                for horizontal in range(0, (rows+1)*columns):

                                    if hs[horizontal]==1: continue

                                    copyh=hs[:]
                                    copyv=vs[:]

                                    copyh[horizontal]=1

                                    ## completed_squares HAS TO BE WRONG. THIS JUST ISN'T WORKING OUT ...
                                    ## but does that and thing improve the situation ???

                                    if completed_squares(hs, vs, rows, columns)==completed_squares(copyh, copyv, rows, columns) and no_consecutive_takeable_squares(copyh, copyv, rows, columns)==2:

                                        ## ie theres a 'neutral' move

                                        is_move_made=True
                                        move_made='h'+str(horizontal)

                                        break

                                for vertical in range(0, (columns+1)*rows):

                                    if vs[vertical]==1: continue

                                    copyh=hs[:]
                                    copyv=vs[:]

                                    copyv[vertical]=1

                                    if completed_squares(hs, vs, rows, columns)==completed_squares(copyh, copyv, rows, columns) and no_consecutive_takeable_squares(copyh, copyv, rows, columns)==2:

                                        ## ie theres a 'neutral' move

                                        is_move_made=True
                                        move_made='v'+str(vertical)

                                        break

                                if is_move_made==False:

                                    move_made=is_winnable_square(hs, vs, rows, columns)
                                    print('can\'t make ;neutral; move')

                                else:
                                  
                                    print('there\'s a neutral move')

                                    ## bit peak but we'll just have to make sacrifices next turn
                        ### THINGS:
                            #else:

                            #        ## okay ... simulate until we can no longer take squares or something?

                            #        chain_size = 0

                            #        if chain_size > 2:

                            #                ## take all but last two
                            #                pass

                            #        else: ## the square is not part of a long chain

                            #                ## hmm ... we should try and not take it!
                            #                move_made = is_winnable_square(vs, hs, rows, columns)

                            ### else take square

                            #pass

                else: ## no winnable squares

                        ## if can play neutral move
                        ## then minimax to try to reach right parity of chains
                        ## (if f(rows*columns + rows + columns) // f(rows*columns) < 10**8: ## is this a good bound ?!)

                        ## else sacrifice the least valuable chain. AND ACTUALLY SACRIFICE IT, NOT JUST LET THEM RETURN THE FAVOR

                        if no_neutrals(hs, vs, rows, columns)>0:

                            ## neutral square to be taken

                            candidate_moves=[]

                            ##print('We\'re making neutral moves')

                            for horizontal in range(0, (rows+1)*columns):

                                if hs[horizontal]==1: continue

                                copyh=hs[:]
                                copyv=vs[:]

                                copyh[horizontal]=1

                                if is_winnable_square(copyh, copyv, rows, columns)==False:
                                    candidate_moves.append('h'+str(horizontal))

                            for vertical in range(0, (columns+1)*rows):

                                if vs[vertical]==1: continue

                                copyh=hs[:]
                                copyv=vs[:]

                                copyv[vertical]=1

                                if is_winnable_square(copyh, copyv, rows, columns)==False:
                                    candidate_moves.append('v'+str(vertical))

                            move_made = candidate_moves[randint(0, len(candidate_moves)-1)]
                            print('random neutral move')
                            
                        else: ## sacrifice least number of squares
                        
                            sacrifice_size = rows*columns ## max possible
                            
                            for horizontal in range(0, (rows+1)*columns):

                                if hs[horizontal] == 1: continue

                                copyh=hs[:]
                                copyv=vs[:]

                                copyh[horizontal]=1

                                if no_consecutive_takeable_squares(copyh, copyv, rows, columns) <= sacrifice_size:

                                    sacrifice_size=no_consecutive_takeable_squares(copyh, copyv, rows, columns)

                                    move_made = 'h'+str(horizontal)

                            for vertical in range(0, (columns+1)*rows):

                                if vs[vertical] == 1: continue

                                copyh=hs[:]
                                copyv=vs[:]

                                copyv[vertical]=1

                                if no_consecutive_takeable_squares(copyh, copyv, rows, columns) <= sacrifice_size:

                                    sacrifice_size=no_consecutive_takeable_squares(copyh, copyv, rows, columns)

                                    move_made = 'v'+str(vertical)
                                    
                            print('sacrifices have to be made')

        completed = completed_squares(hs, vs, rows, columns) ## prior completed squares

        if move_made[0] == 'h':

                hs[int(move_made[1:])] = 1

        if move_made[0] == 'v':

                vs[int(move_made[1:])] = 1

        if completed_squares(hs, vs, rows, columns) > completed: ## rotate turn

                our_completed_squares[players_turn] += completed_squares(hs, vs, rows, columns)-completed

        else: ## rotate turn

                players_turn+=1
                players_turn=players_turn%2
                
print('You took', our_completed_squares[0], 'squares')
print('The computer took', our_completed_squares[1], 'squares')

if our_completed_squares[0]>our_completed_squares[1]:
  print('You win!')
  
if our_completed_squares[1]>our_completed_squares[0]:
  print('You lose!')
  
if our_completed_squares[0]==our_completed_squares[1]:
  print('It\'s a draw!')
