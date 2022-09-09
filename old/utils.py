# Utility functions for drawing. Unused now.

from constants import *

from PIL import Image, ImageDraw

def in_bounds(r, c, grid):
    R, C = len(grid), len(grid[0])
    return 0 <= r < R and 0 <= c < C

def has_wall(cell, direction):
    return cell & direction == 0

'''
Print maze as ASCII art. Walls are '_' and '|'
Cells are ' '.
'''
def print_maze(grid):
    R, C = len(grid), len(grid[0])
    print(' ' + '_' * (2*C - 1)) # top row
    for r in range(R):
        print('|', end='') # leftmost wall
        for c in range(C):
            # check for south wall
            if has_wall(grid[r][c], S):
                print('_', end='')
            else:
                print(' ', end='')

            # check for east wall
            if c == C-1 or has_wall(grid[r][c], E):
                print('|', end='')
            else:
                print(' ' , end='')
        print()

'''
Render a maze to a PNG file. `filename` should exclude the extension.
Example invocation: `write_maze_to_image(grid, "img-recursive-backtracking")`
'''
def write_maze_to_image(grid, filename):
    SC = 25 # output scale
    M = 0 # padding

    R, C = len(grid), len(grid[0])
    W, H = C*SC, R*SC

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    image = Image.new('RGB', (W + 2*M, H + 2*M))
    draw = ImageDraw.Draw(image)

    draw.rectangle([(M, M),
                    (M + W, M + H)],
                    WHITE)

    for r in range(R):
        for c in range(C):
            if has_wall(grid[r][c], E):
                draw.line([(M + (c+1)*SC, M + r*SC),
                           (M + (c+1)*SC, M + (r+1)*SC)],
                           BLACK)
            if has_wall(grid[r][c], S):
                draw.line([(M + c*SC, M + (r+1)*SC),
                           (M + (c+1)*SC, M + (r+1)*SC)],
                           BLACK)

    del draw
    image.save(f"./img/{filename}", 'PNG')