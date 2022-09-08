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
    carve_passages_from(0, 0, None, grid)
    return grid

'''
Iteratively carve out connections from cell cx, cy depth-first.
`reverse_dir` is the direction from cx, cy to the earlier cell that enqueued it.
Initially, `reverse_dir` == None
All callers must ensure that `cy` is a valid row index
and `cx` is a valid col index for `grid`.
'''
def carve_passages_from(cx, cy, reverse_dir, grid):
    dirs = [N, E, W, S]

    w, h = len(grid[0]), len(grid)
    stack = [(cx, cy, reverse_dir)]
    seen = [[False for _ in range(w)] for _ in range(h)]

    while stack:
        cx, cy, reverse_dir = stack.pop()
        if seen[cy][cx]:
            continue
        seen[cy][cx] = True

        if reverse_dir:
            px, py = cx + DX[reverse_dir], cy + DY[reverse_dir]
            prev_dir = OPPOSITE[reverse_dir]
            grid[py][px] |= prev_dir
            grid[cy][cx] |= reverse_dir

        shuffle(dirs) # shuffle to create a new path each time
        for new_dir in dirs:
            nx, ny = cx + DX[new_dir], cy + DY[new_dir]

            if not in_bounds(ny, nx, grid):
                continue
        
            stack.append((nx, ny, OPPOSITE[new_dir]))


# Around (47, 47) you'll occasionally see recursion depth exceeded errors
# across multiple runs. The max stack depth is the length of the longest path
# within the generated maze. This is random since we shuffle the directions arr.
maze = generate_maze(5, 5)
print_maze(maze)
write_maze_to_image(maze, "iterative-backtracking")