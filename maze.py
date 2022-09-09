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
    Returns True iff the cell represented by `coords` lies within
    the maze. `coords` is a list of integers. For a Cartesian maze this would be
    a list of 2 integers. For a hex maze using cube coordinates this would be a
    list of 3 integers.
    '''
    def in_bounds(self, coords):
        raise NotImplementedError("Abstract method `in_bounds` must be implemented")

    '''
    Returns True iff the cell represented by `coords` has a wall in the direction
    `direction`. `coords` is a list of integers and `direction`'s representation
    depends on the kind of maze.
    '''
    def has_wall(self, coords, direction):
        raise NotImplementedError("Abstract method `has_wall` must be implemented")

    def neighbors(self, coords):
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