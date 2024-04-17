import numpy as np

from mazes import SquareMaze

m = 20
n = 20
num_sides = 4
walls = np.zeros((m, n, int(num_sides/2)), dtype=bool)
walls[2:5, 4, 0] = walls[1, 4, 1] = walls[4, 4, 1] = walls[2, 2, 1] = walls[3, 2, 1] = True
smile_maze = SquareMaze(walls)
full_maze = SquareMaze(np.full((m, n, int(num_sides/2)), 1, dtype=bool))

full_maze.plot().savefig("filled.png")
smile_maze.plot().savefig("smile.png")
