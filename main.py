from cartesian_maze import CartesianMaze
# from pointy_hexagon_maze import PointyHexagonMaze

if __name__ == '__main__':
    maze = CartesianMaze(50)
    maze.generate()
    maze.render_to_text()
    maze.render_to_png('iterative-backtracking')