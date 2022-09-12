from maze import Maze

from PIL import Image, ImageDraw
from random import shuffle

N, S, E, W = 1, 2, 4, 8
SEEN_MARKER = 16 # when this is set, the cell is seen

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
        self.rows = side
        self.cols = side
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def __in_bounds(self, coords):
        r, c = coords
        return 0 <= r < self.rows and 0 <= c < self.cols

    '''
    When the bitwise AND of a cell and a direction is 0 it means there is no
    connection in that direction, which means there is a wall there. This method
    assumes that `coords` is known to be in bounds.
    '''
    def __has_wall(self, coords, direction):
        r, c = coords
        return self.grid[r][c] & direction == 0

    def render_to_text(self):
        print(' ' + '_' * (2*self.cols - 1)) # top row
        for r in range(self.rows):
            print('|', end='') # leftmost wall
            for c in range(self.cols):
                # check for south wall
                if self.__has_wall([r, c], S):
                    print('_', end='')
                else:
                    print(' ', end='')

                # check for east wall
                if c == self.cols-1 or self.__has_wall([r, c], E):
                    print('|', end='')
                else:
                    print(' ' , end='')
            print()

    def render_to_png(self, filename):
        SC = 25 # output scale
        M = 20 # padding

        WIDTH, HEIGHT = self.cols*SC, self.rows*SC

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        image = Image.new('RGB', (WIDTH + 2*M, HEIGHT + 2*M))
        draw = ImageDraw.Draw(image)

        draw.rectangle([(0, 0),
                        (WIDTH + 2*M, HEIGHT + 2*M)],
                        WHITE)
        draw.rectangle([(M, M), (WIDTH + M, HEIGHT + M)], None, BLACK)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.__has_wall([r, c], E):
                    draw.line([(M + (c+1)*SC, M + r*SC),
                               (M + (c+1)*SC, M + (r+1)*SC)],
                               BLACK)
                if self.__has_wall([r, c], S):
                    draw.line([(M + c*SC, M + (r+1)*SC),
                               (M + (c+1)*SC, M + (r+1)*SC)],
                               BLACK)

        del draw

        path = f"./img/{filename}.png"
        print(f"Writing maze to {path}")
        image.save(f"{path}", 'PNG')

    def __neighbors(self, coords):
        directions = [N, E, W, S]
        shuffle(directions)

        cx, cy = coords

        for direction in directions:
            nx, ny = cx + DX[direction], cy + DY[direction]

            if not self.__in_bounds([ny, nx]):
                continue

            yield (nx, ny, direction)

    '''
    Generate a maze by carving out passages starting from cell (cx, cy). Here
    `cx` is the row, `cy` is the column.
    '''
    def carve_passages_from(self, cx, cy):
        # We start out with `reverse_dir` == None.
        stack = [(cx, cy, None)]

        while stack:
            # `reverse_dir` is the direction that takes you from the current cell
            # to the cell that enqueued it. This is why we start out the stack
            # with a None `reverse_dir`.
            cx, cy, reverse_dir = stack.pop()
            if self.__seen([cy, cx]):
                continue
            self.__mark_seen([cy, cx])

            if reverse_dir:
                px, py = cx + DX[reverse_dir], cy + DY[reverse_dir]
                prev_dir = OPPOSITE[reverse_dir]
                self.grid[py][px] |= prev_dir
                self.grid[cy][cx] |= reverse_dir

            for nx, ny, new_dir in self.__neighbors([cx, cy]):
                stack.append((nx, ny, OPPOSITE[new_dir]))

    def generate(self):
        self.carve_passages_from(0, 0) # top-leftmost cell

    def __seen(self, coords):
        cy, cx = coords
        return self.grid[cy][cx] & SEEN_MARKER != 0

    def __mark_seen(self, coords):
        cy, cx = coords
        self.grid[cy][cx] |= SEEN_MARKER
