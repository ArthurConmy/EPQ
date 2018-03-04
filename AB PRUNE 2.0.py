import time
T=time.time()

game_tree=[[], [[[], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], 1, 0, 0, -1], [[], [0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], 1, 0, 0, -1]]]

## game_tree[depth_index][leaf_index][0] is list of the leaf_index of the leaf's parentS - note the plural that should make the bloody program actually run
## game_tree[depth_index][leaf_index][1] are the horizontals (list) 
## game_tree[depth_index][leaf_index][2] are the verticals (list) 
## game_tree[depth_index][leaf_index][3] is the player-who-has-just-made-a-move's turn. But I think it's next players turrn ...
## game_tree[depth_index][leaf_index][4] is player 0's no. squares won
## game_tree[depth_index][leaf_index][5] is player 1's no. squares won
## game_tree[depth_index][leaf_index][6] player who has won (False if still open game) - not yet actually used

def isin(big, small):
    for thing in big:
        if thing[1:]==small[1:]:
            return big.index(thing)
    return -1

def deep_copy(lis):
    new_lis=[]
    for elem in lis:
        if type(elem)==list:
            new_lis.append(deep_copy(elem))
        else:
            new_lis.append(elem)
    return new_lis

def completed_squares(verticals, horizontals, bs=2): ## Returns the number of completed squares (all players)

    the_completed_squares=[]
    
    for upper in range(0, len(horizontals)-bs):
        if horizontals[upper]==1 and horizontals[upper+bs]==1 and verticals[upper + upper//bs]==1 and verticals[upper + upper//bs + 1]==1:
            the_completed_squares.append(upper)
                
    return len(the_completed_squares)

for depth in range(2, 13):
    game_tree.append([]) ## the new depth level

    for index in range(0, len(game_tree[depth-1])): ## for leaf in previous level

        current_leaf=deep_copy(game_tree[depth-1][index]) ## this is the leaf we're working with

        ##if current_leaf[6]!=-1: ## if a player has already won, who cares? Actually I think this clears up the simulation after this significantly
            ##continue

        for horizontal in range(0, 6):
            if current_leaf[1][horizontal]==0:
                new_leaf=deep_copy(current_leaf)

                new_leaf[0]=[index] ## this is the parent branch
                
                new_leaf[1][horizontal]=1

                squares_difference=completed_squares(new_leaf[2], new_leaf[1])-completed_squares(current_leaf[2], current_leaf[1])

                if squares_difference>0: ## if squares have been won, we need to know about it
                    new_leaf[4+new_leaf[3]]+=squares_difference

                    if new_leaf[4] > 2: new_leaf[6]=0
                    if new_leaf[5] > 2: new_leaf[6]=1

                else: ## change turn. this means that what we're measuring is *next* turn
                    new_leaf[3]=(new_leaf[3]+1)%2
                    
                if isin(game_tree[-1], new_leaf)==-1:
                    game_tree[-1].append(new_leaf)

                else:
                    new_index=isin(game_tree[-1], new_leaf)
                    game_tree[-1][new_index][0].append(index)

##                game_tree[-1].append(new_leaf)

                ## if this leaf is not already in this layer then
                ## else
                ## then append to the indexs of the original leaf the index of this leaf 

        for vertical in range(0, 6):
            if current_leaf[2][vertical]==0:
                new_leaf=deep_copy(current_leaf)

                new_leaf[0]=[index] ## this is the parent branch
                
                new_leaf[2][vertical]=1

                squares_difference=completed_squares(new_leaf[2], new_leaf[1])-completed_squares(current_leaf[2], current_leaf[1])

                if squares_difference>0: ## if squares have been won, we need to know about it
                    new_leaf[4+new_leaf[3]]+=squares_difference

                    if new_leaf[4] > 2: new_leaf[6]=0
                    if new_leaf[5] > 2: new_leaf[6]=1

                else: ## change turn
                    new_leaf[3]=(new_leaf[3]+1)%2

##                if new_leaf[4]>=3:
##                    new_leaf[6]=0
##
##                if new_leaf[5]>=3:
##                    new_leaf[6]=1
                
                if isin(game_tree[-1], new_leaf)==-1:
                    game_tree[-1].append(new_leaf)

                else:
                    new_index=isin(game_tree[-1], new_leaf)
                    game_tree[-1][new_index][0].append(index)

##                game_tree[-1].append(new_leaf)

    print('Finished depth', depth, 'after', int(time.time()-T), 'seconds')

for depth in range(12, 1, -1):

    for leaf in game_tree[depth]:

        if leaf[6]!=-1:

            if leaf[3] == leaf[6]: ## the player who has won is the same as the player who has just made the move

                for index in leaf[0]:

                    game_tree[depth-1][index][6] = leaf[3]

                    ##print('Okay, since at depth', depth, 'and leaf being', game_tree[depth].index(leaf), 'there\'s a win, there\'s also win at', index, 'the depth below')

##for depth in range(1, 13): ## this section prints out the number of wins at the depths. worryingly asymmetrical ???
##
##    ##print('At depth', depth, end='')
##
##    counts=[0, 0, 0]
##
##    for leaf in game_tree[depth]:
##
##        counts[leaf[6]] += len(leaf[0])
##
##    ##print(' {} wins for 0, {} wins for 1 and {} draws'.format(counts[0], counts[1], counts[2]))

game_state=deep_copy(game_tree[1][0]) ## maybe change to [1][1] later

turn=1 ## ie its the players turn since we went first

for line in range(2, 13): ## the line that we're *drawing* NOW

    print('Game state is', game_state)

    if turn==0: ## AI turn

        print('AI\'s turn!')

        ## find the index in game_tree[line-1]

        ## for leaf in game_tree[line]

        ## if leaf[6] == 0

        ## make that move
        ## flip turn if needed

        ## else make a move at random
        ## flip turn if needed

        for index in range(0, len(game_tree[line-1])):

            if game_state[1:] == game_tree[line-1][index][1:]: ## found the index

                print('The index of that game_state is', index)
                stem_index = index
                break

        this_is_the_first = True ## this ensures that we get at least one new_move, even if it causes our loss

        for leaf in game_tree[line]:

            if stem_index not in leaf[0]: continue

            ##if leaf[3] != 0: continue ## not the AI's move. actually I don't that it's working like this. 

            if this_is_the_first or leaf[6] != 1: ## this stops the AI from choosing moves that cause our loss
                new_move = deep_copy(leaf)

            if leaf[6] == 0: ## so we always make a new move, but if we win from one of these moves then we break
                break

            this_is_the_first = False

        if completed_squares(new_move[2], new_move[1]) == completed_squares(game_state[2], game_state[1]):
                ## that is, no squares have been won

                ##print('Turns flip')
            turn = (turn + 1) % 2

        game_state = new_move

    else: ## player's turn

        print('Player\'s turn!')

        ## get input of turn

        ## make copy of game_state, make move on it

        ## change all copy things to what they should be

        ## flip turn if needed

        move = input('Enter legal move >')

        new_game_state = deep_copy(game_state)

        if move[0] == 'h':
            new_game_state[1][int(move[1:])] = 1
            print('got h')

        if move[0] == 'v':
            new_game_state[2][int(move[1:])] = 1
            print('got v')

        new_game_state[3] = 1 ## player 1 has just made a move

        if completed_squares(new_game_state[2], new_game_state[1]) == completed_squares(game_state[2], game_state[1]):
            ## no squares won

            turn = (turn + 1) % 2

        else:

            new_game_state[5] += completed_squares(new_game_state[2], new_game_state[1]) - completed_squares(game_state[2], game_state[1])

        new_game_state[3]=turn

        for leaf in game_tree[line]:

            if new_game_state[1:-1] == leaf[1:-1]:

                game_state = leaf
                print('Found the game state!')
                break

        else:
            print('Oh dear.') ## why does this fire? why are some game states not present in game_tree?
            print(new_game_state)
            input()
