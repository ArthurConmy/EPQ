from itertools import count
from math import factorial as f

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

def completed_squares(hs, vs, rs, cs): ## Returns the number of completed squares (all players)

    the_completed_squares=0 ##=[]
    
    for upper in range(0, rs*cs): ## dependent on board_size !!!
        if hs[upper]==1 and hs[upper+cs]==1 and vs[upper + upper//cs]==1 and vs[upper + upper//cs + 1]==1:
            the_completed_squares+=1 ##.append(upper)
                
    return the_completed_squares ## used to be len

rows = 2
columns = 3

hs=[0 for i in range(0, columns*(rows+1))]
vs=[0 for i in range(0, rows*(columns+1))]

no_players=2

our_completed_squares=[0 for i in range(0, no_players)]

players_turn=0

for turn in count():

        ##move_made = False

        if players_turn == 0:

        ## players turn

        ## code from simulator or wherever

                move_made = input('It\'s your move, player! >')

        else: ## AI turn

                if f(rows*columns + rows + columns) // f(rows*columns) < 10**8: ## is this a good bound ?!

                        ## we can minimax for critical state, check for parity of chains

                        pass

                else:

                        if is_winnable_square(hs, vs, rs, cs)!=False: ## we can take a square!! though the way below to take that square may be bad ...

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
