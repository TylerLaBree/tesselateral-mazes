import numpy as np

import mazes

m = 3
n = 3
num_sides = 4
walls = np.zeros((m, n, int(num_sides/2)), dtype=bool)
empty_maze = mazes.SquareMaze(walls)
print(empty_maze.walls)