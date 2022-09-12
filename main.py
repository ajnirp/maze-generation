from cartesian_maze import CartesianMaze
from pointy_hexagon_maze import PointyHexagonMaze
from triangle_maze import TriangleMaze

if __name__ == '__main__':
    maze = CartesianMaze(50)
    maze.generate()
    # maze.render_to_text()
    maze.render_to_png('cartesian')

    maze = PointyHexagonMaze(15)
    maze.generate()
    maze.render_to_png('hex')

    maze = TriangleMaze(20)
    maze.generate()
    # maze.render_to_png('triangle')