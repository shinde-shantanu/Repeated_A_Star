from Grid_Generator import gen_grid
import timeit
import pandas as pd

def dist(i, j, dim, heu): #function to measure heuristic values
    if heu == 1:
        return ( ((i-dim-1) ** 2) + ((j-dim-1) ** 2) ) ** 0.5 #Euclidean distance
    if heu == 2:
        return abs(dim-1-i)+abs(dim-1-j) #Manhattan distance
    if heu == 3:
        return max(abs(i-dim-1),abs(j-dim-1)) #Chebychev distance

def insert_fringe(i, j, fringe, f): #insertion into priority queue (Fringe)
    #print(fringe)
    if len(fringe)==0:
        fringe.append((i,j))
    else:
        for x in range(len(fringe)):
            (I,J)=fringe[x]
            if f[I][J]>f[i][j]:
                fringe.insert(x, (i,j))
                return
        fringe.append((i,j))

def find_path(parent, dim, si, sj): #used to find the path from the parent data structure
    i,j = dim-1, dim-1
    path = [(dim-1, dim-1)]
    while (i, j) != (si, sj):
        path.insert(0, parent[i][j])
        (i, j) = parent[i][j]
    return(path)

def search_size(parent, dim): #used to find the size of the search tree that was discovered
    ans = 0
    for i in parent:
        for j in i:
            if j == -1:
                ans = ans + 1
    return ((dim * dim) - ans)

def a_star(dim, P, grid, heu, si, sj):
    
    result=False
    
    g=[[-1 for i in range(dim)] for j in range(dim)] #data structure to store g(n) (list of lists). initialized with -1 for now
    g[si][sj]=0
    
    h=[[dist(i,j,dim,heu) for i in range(dim)] for j in range(dim)] #data structure to store h(n) (list of lists).
    
    f=[[-1 for i in range(dim)] for j in range(dim)] #data structure to store f(n) (list of lists). initialized with -1 for now
    f[si][sj]=g[si][sj]+h[si][sj]
    p=[[-1 for i in range(dim)] for j in range(dim)] #data structure to store pointers to parent (list of lists). initialized with -1 for now
    p[si][sj]=0
    
    fringe=[(si,sj)] #pushing the start node into the fringe
    
    while len(fringe)!=0:
        (i,j)=fringe.pop(0)
        if (i,j) == (dim-1,dim-1): #true if goal node is reached
            result=True
            break
        #print((i,j))
        if i-1 >= 0 and grid[i-1][j] != 1 and p[i-1][j]==-1 and p[i][j] != (i-1,j): #checking the chilren of each node popped from fringe
            p[i-1][j]=(i,j)
            g[i-1][j]=g[i][j]+1
            f[i-1][j]=g[i-1][j]+h[i-1][j]
            insert_fringe(i-1,j,fringe,f)
            
        if j+1 < dim and grid[i][j+1] != 1 and p[i][j+1]==-1 and p[i][j] != (i,j+1):
            p[i][j+1]=(i,j)
            g[i][j+1]=g[i][j]+1
            f[i][j+1]=g[i][j+1]+h[i][j+1]
            insert_fringe(i,j+1,fringe,f)
            
        if i+1 < dim and grid[i+1][j] != 1 and p[i+1][j]==-1 and p[i][j] != (i+1,j):
            p[i+1][j]=(i,j)
            g[i+1][j]=g[i][j]+1
            f[i+1][j]=g[i+1][j]+h[i+1][j]
            insert_fringe(i+1,j,fringe,f)
            
        if j-1 >= 0 and grid[i][j-1] != 1 and p[i][j-1]==-1 and p[i][j] != (i,j-1):
            p[i][j-1]=(i,j)
            g[i][j-1]=g[i][j]+1
            f[i][j-1]=g[i][j-1]+h[i][j-1]
            insert_fringe(i,j-1,fringe,f)
    
    return(result, p)

def lim_repeated_a_star(grid, dim, P, heu):
    
    start = timeit.default_timer() #recording time stamp to measure run time
    
    dis = [[0 for i in range(dim)] for j in range(dim)] #used to represent the gridworld that has been discovered (list of lists)
    
    result = False
    done = False
    
    si = 0 #Co-ordinates of the start node
    sj = 0
    
    final = [] #Data structure to store final trajectory
    
    cells = 0
    
    while done != True:
        
        result, parent =a_star(dim, P, dis, heu, si, sj) #planning stage of repeated A*
        if result == False: #true if grid not solvable
            break
        
        path = find_path(parent, dim, si, sj)
        cells = cells + search_size(parent, dim) #used to record total number of cells processed
        
        flag = True
        for (i, j) in path: #agent traversing the planned path
            if grid[i][j] == 1: #only updating the grid knowledge after agent bumps into a blocked node
                dis[i][j] = 1
                (si, sj) = parent[i][j]
                final.pop(len(final)-1)
                flag = False
                break
            final.append((i, j))

        if flag:
            done = True
    
    stop = timeit.default_timer()
    
    return(result, final, dis, cells, start, stop) #recording time stamp to measure run time

df = pd.DataFrame(columns=['p',
                           'Trajectory Length',
                           'FDG Length',
                           'FG Length',
                           'Cells Processed'])

p = 0

x = 0

while p < 0.31: #recording values between 0.01 <= p < 0.31
    
    grid = gen_grid(101, p) #generating grid
    
    result, traj, dis, cells_processed, start, stop = lim_repeated_a_star(grid, 101, p, 2) #running limited repeated A* on the generated grid
    
    if result:
        x = x + 1
        result, parent = a_star(101, p, dis, 2, 0, 0) #running A* on the final discovered grid
        FDG_path = find_path(parent, 101, 0, 0) #Shortest Path in Final Discovered Gridworld
        
        result, parent = a_star(101, p, grid, 2, 0, 0) #running A* on the full gridworld
        FG_path = find_path(parent, 101, 0, 0) #ShortestPath in Full Gridworld
        
        df1 = pd.DataFrame([[p, len(traj), len(FDG_path), len(FG_path), cells_processed]],columns=['p','Trajectory Length','FDG Length','FG Length','Cells Processed'])
        df = pd.concat([df,df1])

    if x == 100:
        x = 0
        print(p)
        p = p + 0.01
        df.to_csv('Question_7.csv')
