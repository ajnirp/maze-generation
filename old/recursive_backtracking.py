# Python port of https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking.html

from constants import *
from utils import *

from random import shuffle

'''
Return a 2D array representing a maze. Each element is an int.
Each cell is a bitfield. Let c be a cell. c | N != 0 means that
the cell has a connection to the cell above it. Initially the
grid starts with all cells 0, meaning no connections. Connections
are made via the carve_passages_from function.
'''
def generate_maze(w, h):
    grid = [[0 for _ in range(w)] for _ in range(h)]
    carve_passages_from(0, 0, grid)
    return grid

'''
Recursively carve out connections from cell cx, cy.
All callers must ensure that `cy` is a valid row index
and `cx` is a valid col index for `grid`.
'''
def carve_passages_from(cx, cy, grid):
    dirs = [N, E, W, S]
    shuffle(dirs) # shuffle to create a new path each time

    for dir_ in dirs:
        nx, ny = cx + DX[dir_], cy + DY[dir_]

        if not in_bounds(ny, nx, grid):
            continue

        # neighbor has already been visited
        if grid[ny][nx] != 0:
            continue
        
        grid[cy][cx] |= dir_
        grid[ny][nx] |= OPPOSITE[dir_]
        
        # recurse. no bounds check needed; it was already done
        carve_passages_from(nx, ny, grid)


# Around (47, 47) you'll occasionally see recursion depth exceeded errors
# across multiple runs. The max stack depth is the length of the longest path
# within the generated maze. This is random since we shuffle the directions arr.
maze = generate_maze(5, 5)
print_maze(maze)
write_maze_to_image(maze, "recursive-backtracking")