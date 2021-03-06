from Repeated_BFS import repeated_BFS
from Repeated_BFS import BFS
from A_Star import a_star
from Grid_Generator import gen_grid
import pandas as pd

def find_path(parent, dim):
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

while p < 0.31:
    
    grid = gen_grid(101, p)
    
    result, traj, dis, cells_processed, start, stop = repeated_BFS(grid, 101)
    
    if result:
        x = x + 1
        result, parent, c = BFS(101, dis, 0, 0)
        FDG_path = find_path(parent, 101)
        
        result, parent, c = BFS(101, grid, 0, 0)
        FG_path = find_path(parent, 101)
        
        df1 = pd.DataFrame([[p, len(traj), len(FDG_path), len(FG_path), cells_processed]],columns=['p','Trajectory Length','FDG Length','FG Length','Cells Processed'])
        df = pd.concat([df,df1])

    if x == 100:
        x = 0
        print(p)
        p = p + 0.01
        df.to_csv('Extra_Question_6.csv')
