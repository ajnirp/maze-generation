# Reference: https://www.redblobgames.com/grids/hexagons/

from maze import Maze

from PIL import Image, ImageDraw
from random import shuffle

NW, NE, E, SE, SW, W = 1, 2, 4, 8, 16, 32
SEEN_MARKER = 64 # when this is set, the cell is seen

DQ = {
    NW: 0,
    SE: 0,

    NE: 1,
    E: 1,

    W: -1,
    SW: -1,
}

DR = {
    NW: -1,
    NE: -1,

    W: 0,
    E: 0,

    SW: 1,
    SE: 1,
}

OPPOSITE = {
    E: W,
    W: E,

    NW: SE,
    SE: NW,

    NE: SW,
    SW: NE,
}

'''
Maze based on a grid with pointy hexagons i.e. regular hexagons in which the
vertices make angles of 30, 90, 150, 210, 270, 330 degrees with the horizontal.
The overall shape of the grid is a flat hexagon. See https://www.redblobgames.com/grids/hexagons/
'''
class PointyHexagonMaze(Maze):
    # Hexagonal grid with side length `N` will have a total of
    # N + (N + 1) + ... [N terms] +
    # N + (N + 1) + ... [N - 1 terms]
    # which comes out to be N^2 + N(N-1) + (N-1)^2
    def __init__(self, side):
        super().__init__(side)
        self.N = side
        self.rows = 2*self.N - 1 # number of rows in the grid

        self.grid = [
            [0 for _ in range(self.rows - abs(self.N - r - 1))]
            for r in range(self.rows)
        ]

    def in_bounds(self, coords):
        q, r = coords
        # in the r-th row, the number of elements is
        # 2*N - 1 - abs(N-r-1)
        # and the q-index goes from 
        # e.g. if side == 3, the rows have these many elements
        # (term becomes 5 - abs(2-r))
        # r 0 => 3 => 2 3 4
        # r 1 => 4 => 1 2 3 4
        # r 2 => 5 => 0 1 2 3 4
        # r 3 => 4 => 0 1 2 3
        # r 4 => 3 => 0 1 2

        d = self.N - r - 1 # signed distance of the row from the center row
        return 0 <= r < self.rows - 1 and max(0, d) <= q < self.rows - abs(d) + max(0, d)

    def neighbors(self, coords):
        directions = [NW, NE, E, SE, SW, W]
        shuffle(directions)

        cq, cr = coords

        for direction in directions:
            nq, nr = cq + DQ[direction], cr + DR[direction]

            if not self.in_bounds([nq, nr]):
                continue

            yield (nq, nr, direction)

    '''
    Generate a maze by carving out passages starting from cell (cq, cr). Here
    `cq` is the q-coordinate, `cr` is the r-coordinate.
    '''
    def carve_passages_from(self, cq, cr):
        # We start out with `reverse_dir` == None.
        stack = [(cq, cr, None)]

        while stack:
            # `reverse_dir` is the direction that takes you from (cx, cy) to the
            # cell that enqueued it. This is why we start out the stack with a
            # None `reverse_dir`.
            cq, cr, reverse_dir = stack.pop()
            if self.__seen([cq, cr]):
                continue
            self.__mark_seen([cq, cr])

            if reverse_dir:
                pq, pr = cq + DQ[reverse_dir], cr + DR[reverse_dir]
                prev_dir = OPPOSITE[reverse_dir]
                self.__carve_passage(pq, pr, prev_dir)
                self.__carve_passage(cq, cr, reverse_dir)

            for nq, nr, new_dir in self.neighbors([cq, cr]):
                stack.append((nq, nr, OPPOSITE[new_dir]))

    def generate(self):
        self.carve_passages_from(self.N-1, 0) # top-leftmost cell

    def __seen(self, coords):
        row, col = self.__coords(*coords)
        return self.grid[row][col] & SEEN_MARKER != 0

    def __mark_seen(self, coords):
        row, col = self.__coords(*coords)
        self.grid[row][col] |= SEEN_MARKER

    '''
    Break the wall at cell `(q, r)` in the direction `direction`.
    '''
    def __carve_passage(self, q, r, direction):
        row, col = self.__coords(q, r)
        self.grid[row][col] |= direction

    '''
    Translate axial coordinates into 2D-array row-column coordinates. We're using
    "array of arrays" storage.
    Reference: https://www.redblobgames.com/grids/hexagons/#map-storage
    '''
    def __coords(self, q, r):
        return r, q - max(0, self.N - r - 1)

'''
Scratchpad

N 3
# r 0 => 3 => 2 3 4
# r 1 => 4 => 1 2 3 4
# r 2 => 5 => 0 1 2 3 4
# r 3 => 4 => 0 1 2 3
# r 4 => 3 => 0 1 2

r, N - r - 1, max(0, 2nd) == min q, max q
0 2 2 2 4
1 1 1 1 4
2 0 0 0 4
3 -1 0 0 3
4 -2 0 0 2

0 <= q - min_q < 2N - 1 - abs(N-r-1)
min_q = max(0, N-r-1)
max(0, N-r-1) <= q < 2N - 1 - abs(N-r-1) + max(0, N-r-1)
'''