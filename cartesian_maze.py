from maze import Maze

from PIL import Image, ImageDraw
from random import shuffle

N, S, E, W = 1, 2, 4, 8
SEEN_MARKER = 16

DX = {
    E: 1,
    W: -1,
    N: 0,
    S: 0,
}

DY = {
    N: -1,
    S: 1,
    E: 0,
    W: 0,
}

OPPOSITE = {
    N: S,
    E: W,
    W: E,
    S: N,
}

'''
Maze based on a 2D square grid.
'''
class CartesianMaze(Maze):
    def __init__(self, side):
        super().__init__(side)
        self.rows = side
        self.cols = side
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def in_bounds(self, coords):
        r, c = coords
        return 0 <= r < self.rows and 0 <= c < self.cols

    '''
    When the bitwise AND of a cell and a direction is 0 it means there is no
    connection in that direction, which means there is a wall there. This method
    assumes that `coords` is known to be in_bounds.
    '''
    def has_wall(self, coords, direction):
        r, c = coords
        return self.grid[r][c] & direction == 0

    def has_east_wall(self, coords):
        return self.has_wall(coords, E)

    def has_south_wall(self, coords):
        return self.has_wall(coords, S)

    def render_to_text(self):
        print(' ' + '_' * (2*self.cols - 1)) # top row
        for r in range(self.rows):
            print('|', end='') # leftmost wall
            for c in range(self.cols):
                # check for south wall
                if self.has_south_wall([r, c]):
                    print('_', end='')
                else:
                    print(' ', end='')

                # check for east wall
                if c == self.cols-1 or self.has_east_wall([r, c]):
                    print('|', end='')
                else:
                    print(' ' , end='')
            print()

    def render_to_png(self, filename):
        SC = 25 # output scale
        M = 0 # padding

        W, H = self.cols*SC, self.rows*SC

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        image = Image.new('RGB', (W + 2*M, H + 2*M))
        draw = ImageDraw.Draw(image)

        draw.rectangle([(M, M),
                        (M + W, M + H)],
                        WHITE)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.has_east_wall([r, c]):
                    draw.line([(M + (c+1)*SC, M + r*SC),
                               (M + (c+1)*SC, M + (r+1)*SC)],
                               BLACK)
                if self.has_south_wall([r, c]):
                    draw.line([(M + c*SC, M + (r+1)*SC),
                               (M + (c+1)*SC, M + (r+1)*SC)],
                               BLACK)

        del draw

        path = f"./img/{filename}"
        print(f"Writing maze to {path}.png")
        image.save(f"{path}", 'PNG')

    def neighbors(self, coords):
        directions = [N, E, W, S]
        shuffle(directions)

        cx, cy = coords

        for direction in directions:
            nx, ny = cx + DX[direction], cy + DY[direction]

            if not self.in_bounds([ny, nx]):
                continue

            yield (nx, ny, direction)

    def seen(self, cx, cy):
        return self.grid[cy][cx] & SEEN_MARKER != 0

    def mark_seen(self, cx, cy):
        self.grid[cy][cx] |= SEEN_MARKER

    '''
    Generate a maze by carving out passages starting from cell (cx, cy). Here
    `cx` is the row, `cy` is the column.
    '''
    def carve_passages_from(self, cx, cy):
        # We start out with `reverse_dir` == None. Read below to see why.
        stack = [(cx, cy, None)]

        # Boolean 2D array of cells which have been seen.
        seen = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        while stack:
            # `reverse_dir` is the direction that takes you from (cx, cy) to the
            # cell that enqueued it. This is why we start out the stack with a
            # None `reverse_dir`.
            cx, cy, reverse_dir = stack.pop()
            if self.seen(cx, cy):
                continue
            self.mark_seen(cx, cy)

            if reverse_dir:
                px, py = cx + DX[reverse_dir], cy + DY[reverse_dir]
                prev_dir = OPPOSITE[reverse_dir]
                self.grid[py][px] |= prev_dir
                self.grid[cy][cx] |= reverse_dir

            for nx, ny, new_dir in self.neighbors([cx, cy]):
                stack.append((nx, ny, OPPOSITE[new_dir]))

    def generate(self):
        self.carve_passages_from(0, 0)
