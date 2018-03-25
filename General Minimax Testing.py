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

def parity_long_chains(hs, vs, rs, cs):
  
  ch=hs[:]
  cv=vs[:]
  chain_sizes=[]
  
  while ch.count(0)+cv.count(0)>0:
    
    ## make dumb move
    
    for h in range(0, (rs+1)*cs):
      if ch[h]==0:
        ch[h]=1 
        break
      
    else:
      for v in range(0, (cs+1)*rs):
        if cv[v]==0:
          cv[v]=1 
          break
        
    while is_winnable_square(ch, cv, rs, cs)!=False:
      
      move=is_winnable_square(ch, cv, rs, cs)
      if move[0]=='h':
        ch[int(move[1:])]=1 
      else:
        cv[int(move[1:])]=1 
    
    chain_sizes.append(completed_squares(ch, cv, rs, cs)-completed_squares(hs, vs, rs, cs)-sum(chain_sizes))
    
  long_chains=0 
  
  ##return chain_sizes
  
  for x in chain_sizes:
    if x>2:
      long_chains+=1
  
  return long_chains%2

def isin(big, small):
    for thing in big:
        if thing[1:]==small[1:]:
            return big.index(thing)
    return -1

rows=4
columns=4

hs=[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]
vs=[0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1]

print_game(hs, vs, 4, 4)
print(no_neutrals(hs, vs, 4, 4))

if no_neutrals(hs, vs, rows, columns) <= 8: ## good bound ???

  breadth=[[[[False], hs, vs, 0, 'NA']]] ## initialise BFS. player 0 to move
  
  ## breadth[depth][index][0] is the list of the parents
  ## breadth[depth][index][1] are horizontals
  ## breadth[depth][index][2] are verticals
  ## breadth[depth][index][3] is player who has JUST made a move before this happened; the LAST move
  ## breadth[depth][index][4] is the parity of chains
  
  while len(breadth[-1]) > 0:
    
    ##print(len(breadth))
    ##print_game(breadth[-1][0][1], breadth[-1][0][2], rows, columns)
    ##print(breadth[-1][0][1])
    ##print(breadth[-1][0][2])
    ##print(breadth[-1][0])
    
    new_layer=[]
    
    for index in range(0, len(breadth[-1])): ##leaf in breadth[-1]:
      
      leaf=breadth[-1][index]
      
      for h in range(0, (rows+1)*columns):
        
        if leaf[1][h]==1: continue
      
        copyh=leaf[1][:]
        copyh[h]=1 
        
        if is_winnable_square(copyh, leaf[2][:], rows, columns)==False:
          
          potential=[[index], copyh, leaf[2][:], (leaf[3]+1)%2, 'NA']
          
          if isin(new_layer, potential)!=-1:
            new_layer[isin(new_layer, potential)][0].append(index)
          
          else:  
            new_layer.append(potential)
            
      for v in range(0, (columns+1)*rows):
        
        if leaf[2][v]==1: continue
      
        copyv=leaf[2][:]
        copyv[v]=1 
        
        if is_winnable_square(leaf[1][:], copyv, rows, columns)==False:
          
          potential=[[index], leaf[1][:], copyv, (leaf[3]+1)%2, 'NA']
          
          if isin(new_layer, potential)!=-1:
            new_layer[isin(new_layer, potential)][0].append(index)
          
          else:  
            new_layer.append(potential)
            
    breadth.append(new_layer)
    
  print('BFS complete')  
    
  for i in range(len(breadth)-2, 0, -1):
    
    print(i)
    print()
    
    for leafi in range(0, len(breadth[i])): ##leafi is 'leaf index'
      
      leaf=breadth[i][leafi]
      
      if is_critical(leaf[1], leaf[2], rows, columns)!=False and leaf[-1]=='NA':
        breadth[i][leafi][-1]=parity_long_chains(leaf[1], leaf[2], rows, columns)
      
      ## if leaf[-1]==False: continue ##is_critical(leaf[1], leaf[2], rows, columns)!=True: continue
    
      par = breadth[i][leafi][-1] ##parity_long_chains(leaf[1], leaf[2], rows, columns)
      
      if rows%2==0 and columns%2==0:
        target=(leaf[3]+1)%2
      else:
        target=leaf[3] ## target here is the parity that we want to have
        
      ##print('Leaf is', leaf, 'target is', target)
    
      if par==target: ## the target is right
      
        for ind in leaf[0]:
          
          breadth[i-1][ind][4]=target
          
        continue
      
      if par=='NA' or par==-1:
        
        for ind in leaf[0]:
          
          if breadth[i-1][ind][4]!=target:
            
            breadth[i-1][ind][4]=-1 ## this is basically 'NA'
            
        continue
      
      else:
        
        for ind in leaf[0]:
          
          if breadth[i-1][ind][4]=='NA':
            
            breadth[i-1][ind][4]=(target+1)%2
    
  # for board in breadth[-2]:
    
  #   hs=board[1]
  #   vs=board[2]
    
  #   print_game(hs, vs, 4, 4)
  #   print(parity_long_chains(hs, vs, 4, 4))
  
  if rows%2==0 and columns%2==0:
    true_target = 0
  else:
    true_target = 1
  
  for thing in breadth[1]:
  
    if thing[4]==true_target:
      
      ## find odd one out between hs+vs and thing[1]+thing[2].
      
      for h in range(0, (rows+1)*columns):
        
        if thing[1][h]==1 and hs[h]==0:
          
          move_made='h'+str(h)
          
      for v in range(0, (columns+1)*rows):
        
        if thing[2][v]==1 and vs[v]==0:
          
          move_made = 'v'+str(v)
  
