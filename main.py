from cartesian_maze import CartesianMaze
from hexagonal_maze import HexagonalMaze

if __name__ == '__main__':
    maze = CartesianMaze(500)
    maze.generate()
    maze.render_to_text()
    maze.render_to_png('iterative-backtracking')