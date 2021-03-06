from Repeated_A_Star import repeated_a_star
from A_Star import a_star
from Grid_Generator import gen_grid
import pandas as pd

def find_path(parent, dim): #used to find the path from the parent data structure
    i,j = dim-1, dim-1
    path = [(dim-1,dim-1)]
    while (i,j) != (0,0):
        path.insert(0, parent[i][j])
        (i,j) = parent[i][j]
    return(path)

df = pd.DataFrame(columns=['p',
                           'Trajectory Length',
                           'FDG Length',
                           'FG Length',
                           'Cells Processed'])

p = 0

x = 0

while p < 0.31: #recording values between 0.01 <= p < 0.31
    
    grid = gen_grid(101, p) #generating grid
    
    result, traj, dis, cells_processed, start, stop = repeated_a_star(grid, 101, p, 2) #running repeated A* on the generated grid
    
    if result:
        x = x + 1
        result, s_a, st_a, parent = a_star(101, p, dis, 2) #running A* on the final discovered grid
        FDG_path = find_path(parent, 101) #Shortest Path in Final Discovered Gridworld
        
        result, s_a, st_a, parent = a_star(101, p, grid, 2) ##running A* on the full gridworld
        FG_path = find_path(parent, 101) #ShortestPath in Full Gridworld
        
        df1 = pd.DataFrame([[p, len(traj), len(FDG_path), len(FG_path), cells_processed]],columns=['p','Trajectory Length','FDG Length','FG Length','Cells Processed'])
        df = pd.concat([df,df1])

    if x == 100:
        x = 0
        print(p)
        p = p + 0.01
        df.to_csv('Question_6.csv')
