'''
Maze class from which implementation classes inherit methods.
'''
class Maze:
    '''
    Initialize a maze. `side` = side length. Initially the maze has no pathways.
    '''
    def __init__(self, side):
        self.side = side

    '''
    Returns True iff the cell represented by `coords` lies within the maze.
    `coords` is a list of integers. The interpretation of `coords` is up to the
    implementation class. Examples:
    1. For a Cartesian maze `coords` would be a list of 2 ints.
    2. For a hex maze using cube coordinates `coords` would be a list of 3 ints.
    '''
    def __in_bounds(self, coords):
        raise NotImplementedError("Abstract method `in_bounds` must be implemented")

    '''
    Returns True iff the cell represented by `coords` has a wall in the direction
    `direction`. `coords` is a list of integers and `direction`'s representation
    depends on the kind of maze.
    '''
    def __has_wall(self, coords, direction):
        raise NotImplementedError("Abstract method `__has_wall` must be implemented")

    '''
    Generator function to yield a list of neighbor cells for the cell located at
    # `coords`. Implementations will usually end up calling self.in_bounds(coords).
    '''
    def __neighbors(self, coords):
        raise NotImplementedError("Abstract method `neighbors` must be implemented")

    '''
    Print out a maze as characters.
    '''
    def render_to_text(self):
        raise NotImplementedError("Abstract method `render_to_text` must be implemented")

    '''
    Render a maze to a PNG file.
    '''
    def render_to_png(self, filename):
        raise NotImplementedError("Abstract method `render_to_png` must be implemented")

    '''
    Generate the walls and connections of the maze.
    '''
    def generate(self):
        raise NotImplementedError("Abstract method `generate` must be implemented")

    # Private methods

    '''
    Check if the cell at `coords` was "seen" during maze generation.
    '''
    def __seen(self, coords):
        raise NotImplementedError("Abstract method `__seen` must be implemented")

    '''
    Mark the cell at `coords` as "seen" during maze generation.
    '''
    def __mark_seen(self, coords):
        raise NotImplementedError("Abstract method `__mark_seen` must be implemented")