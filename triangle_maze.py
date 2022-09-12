from maze import Maze

from PIL import Image, ImageDraw
from random import shuffle

SQRT_3 = 1.73205
N, E, S, W = 1, 2, 4, 8
SEEN_MARKER = 16 # when this is set, the cell is seen

DR = {
    N: -1,
    S: 1,
    E: 0,
    W: 0,
}

DQ = {
    W: -1,
    E: 1,
    N: 0,
    S: 0,
}

OPPOSITE = {
    N: S,
    S: N,
    E: W,
    W: E,
}

'''
Maze based on a grid made of equilateral triangles
The overall shape of the grid is an equilateral triangle pointing up
`coords` is a list of length 2 representing [r, q] coordinates.
'''
class TriangleMaze(Maze):
    def __init__(self, side):
        self.N = side # number of rows in the grid

        # Grid is stored as an array of arrays
        self.grid = [
            [0 for _ in range(2*r + 1)]
            for r in range(self.N)
        ]

    def __in_bounds(self, coords):
        r, q = coords
        return 0 <= r < self.N and -r <= q <= r

    def __points_up(self, r, q):
        return (r + q) % 2 == 0

    def __neighbors(self, coords):
        directions = [E, W]
        directions.append(S if self.__points_up(*coords) else N)
        shuffle(directions)

        cr, cq = coords

        for direction in directions:
            nr, nq = cr + DR[direction], cq + DQ[direction]

            if not self.__in_bounds([nr, nq]):
                continue

            yield (nr, nq, direction)

    def render_to_png(self, filename):
        SC = 40 # output scale
        M = 25 # padding

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        WIDTH = int(self.N*SC) # final row has width == N triangles
        HEIGHT = int(SQRT_3*WIDTH/2)

        image = Image.new('RGB', (WIDTH + 2*M, HEIGHT + 2*M))
        draw = ImageDraw.Draw(image)

        draw.rectangle([(0, 0),
                        (WIDTH + 2*M, HEIGHT + 2*M)],
                        WHITE)

        # draw the boundary of the overall grid
        draw.polygon([(M+WIDTH/2, M),
                      (M, M+HEIGHT),
                      (M+WIDTH, M+HEIGHT)],
                     None, BLACK)

        for r in range(self.N):
            for q in range(-r, r+1):
                if self.__points_up(r, q):
                    if self.__has_wall([r, q], E):
                        draw.line([(M+(WIDTH+q*SC)/2, M+SC*(r*SQRT_3/2)),
                                   (M+(WIDTH+(q+1)*SC)/2, M+SC*((r+1)*SQRT_3/2))],
                                  BLACK)
                    if self.__has_wall([r, q], S):
                        draw.line([(M+(WIDTH+(q-1)*SC)/2, M+SC*((r+1)*SQRT_3/2)),
                                   (M+(WIDTH+(q+1)*SC)/2, M+SC*((r+1)*SQRT_3/2))],
                                  BLACK)
                else:
                    if self.__has_wall([r, q], E):
                        draw.line([(M+(WIDTH+(q+1)*SC)/2, M+SC*(r*SQRT_3/2)),
                                   (M+(WIDTH+q*SC)/2, M+SC*((r+1)*SQRT_3/2))],
                                  BLACK)

        del draw

        path = f"./img/{filename}.png"
        print(f"Writing maze to {path}")
        image.save(f"{path}", 'PNG')

    def carve_passages_from(self, cr, cq):
        # We start out with `reverse_dir` == None.
        stack = [(cr, cq, None)]

        while stack:
            # `reverse_dir` is the direction that takes you from the current cell
            # to the cell that enqueued it. This is why we start out the stack
            # with a None `reverse_dir`.
            cr, cq, reverse_dir = stack.pop()
            if self.__seen([cr, cq]):
                continue
            self.__mark_seen([cr, cq])

            if reverse_dir:
                pr, pq = cr + DR[reverse_dir], cq + DQ[reverse_dir]
                prev_dir = OPPOSITE[reverse_dir]
                self.grid[pr][pr+pq] |= prev_dir
                self.grid[cr][cr+cq] |= reverse_dir

            for nq, nr, new_dir in self.__neighbors([cr, cq]):
                stack.append((nq, nr, OPPOSITE[new_dir]))

    def generate(self):
        self.carve_passages_from(0, 0) # topmost cell

    '''
    When the bitwise AND of a cell and a direction is 0 it means there is no
    connection in that direction, which means there is a wall there. This method
    assumes that `coords` is known to be in bounds.
    '''
    def __has_wall(self, coords, direction):
        r, q = coords
        return self.grid[r][r+q] & direction == 0

    def __seen(self, coords):
        r, q = coords
        return self.grid[r][r+q] & SEEN_MARKER != 0

    def __mark_seen(self, coords):
        r, q = coords
        self.grid[r][r+q] |= SEEN_MARKER

'''
Notes

r-q coordinates
         0
      -1 0 1
   -2 -1 0 1 2
-3 -2 -1 0 1 2 3

row-col coordinates
      0
    0 1 2
  0 1 2 3 4
0 1 2 3 4 5 6

r goes from 0 to n-1 inclusive
q goes from -r to r inclusive
row r has 2r + 1 cells
total number of cells is 1 + 3 + 5 ... [n terms] = n^2

r+q is even <=> the cell points up
r+q is odd <=> the cells points down

each cell (r, q) has up to 3 neighbors
if a cell points up, its neighbors are (r+1, q), (r, q+1), (r, q-1)
if a cell points down, its neighbors are (r-1, q), (r, q+1), (r, q-1)

storage is done as an array of arrays
to translate (r, q) to 2D array coords: (r, q) => (r, q+r)
'''