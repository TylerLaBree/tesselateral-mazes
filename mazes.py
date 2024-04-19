import numpy as np
import matplotlib.pyplot as plt
import random
import itertools as it


class SquareMaze:
    """
    Fundamental object class for any maze made up of square cells.
    """
    half_num_sides = 2
    start = None
    end = None

    def __init__(self, wall_map):
        self.wall_map = wall_map
        self.cut_out_of_bounds()
        self.width, self.height, x = self.wall_map.shape
        if self.half_num_sides != x:
            print("ERROR: wall_map shape incorrect")

    def cut_out_of_bounds(self):
        """
        Removes walls which are not in the maze region.
        South-facing walls on the left, and East-facing walls on the top are not needed
        and not used. If the user defined these, remove them.
        """
        self.wall_map[0, :, 0] = False
        self.wall_map[:, 0, 1] = False

    def plot(self):
        """
        Display the square maze using matplotlib.
        """
        xs = np.broadcast_to(
            np.arange(self.width), (self.height, self.width)
        ).transpose()
        ys = np.broadcast_to(np.arange(self.height), (self.width, self.height))

        is_not_hwall = np.logical_not(self.wall_map[:, :, 0])
        plt.hlines(
            ys[self.wall_map[:, :, 0]],
            xs[self.wall_map[:, :, 0]] - 1,
            xs[self.wall_map[:, :, 0]],
            color="black",
        )
        plt.hlines(
            ys[is_not_hwall],
            xs[is_not_hwall] - 1,
            xs[is_not_hwall],
            color="lightgray",
            linestyle="dashed",
        )

        is_not_vwall = np.logical_not(self.wall_map[:, :, 1])
        plt.vlines(
            xs[self.wall_map[:, :, 1]],
            ys[self.wall_map[:, :, 1]] - 1,
            ys[self.wall_map[:, :, 1]],
            color="black",
        )
        plt.vlines(
            xs[is_not_vwall],
            ys[is_not_vwall] - 1,
            ys[is_not_vwall],
            color="lightgray",
            linestyle="dashed",
        )
        if self.start is not None:
            plt.text(
                self.start[0] - 0.5,
                self.start[1] - 0.5,
                "START",
                horizontalalignment="center",
                verticalalignment="center",
            )
        if self.end is not None:
            plt.text(
                self.end[0] - 0.5,
                self.end[1] - 0.5,
                "END",
                horizontalalignment="center",
                verticalalignment="center",
            )
        plt.xticks([])
        plt.yticks([])
        plt.xlim([-0.01, self.width - 1 + 0.01])
        plt.ylim([-0.01, self.height - 1 + 0.01])
        plt.ylim(max(plt.ylim()), min(plt.ylim()))
        plt.axis("off")
        plt.gca().set_aspect("equal")
        return plt


class SquareKruskalMaze(SquareMaze):
    """
    Compound object class for sqaure tiling mazes created using Kruskal's Algorithm.
    """
    def __init__(self, width, height, seed=None):
        self.width = width + 1
        self.height = height + 1
        self.cells = (
            np.indices((self.width, self.height))
            .transpose((2, 1, 0))
            .reshape((self.width * self.height, 1, 2))
        )
        self.walls = (
            np.indices((self.width, self.height, self.half_num_sides))
            .transpose((3, 1, 2, 0))
            .reshape((self.width * self.height * 2, 3))
        )
        self.wall_map = np.full(
            (self.width, self.height, self.half_num_sides), 1, dtype=bool
        )
        self.cut_out_of_bounds()
        self.cut_exterior_walls()
        if seed is not None:
            random.seed(seed)

    def cut_out_of_bounds(self):
        """
        Removes walls and cells which are outside the maze from the various data
        structures used to compute a maze using Kruskal's algorithm
        """
        self.wall_map[0, :, 0] = False
        self.wall_map[:, 0, 1] = False
        wall_filter = np.apply_along_axis(
            lambda xyi: not (xyi[0] == 0 and xyi[2] == 0)
            and not (xyi[1] == 0 and xyi[2] == 1),
            1,
            self.walls,
        )
        self.walls = self.walls[wall_filter]
        cell_filter = np.apply_along_axis(
            lambda xy: xy[0] != 0 and xy[1] != 0, 2, self.cells
        ).reshape((self.width * self.width))
        self.cells = self.cells[cell_filter].tolist()

    def cut_exterior_walls(self):
        """
        Removes exterior walls from the wall list available to Kruskal's algorithm.
        This is because Kruskal's algorithm searches internal walls to remove at random.
        """
        wall_filter = np.apply_along_axis(
            lambda xyi: not (xyi[0] == 0 and xyi[2] == 1)
            and not (xyi[1] == 0 and xyi[2] == 0)
            and not (xyi[0] == self.width - 1 and xyi[2] == 1)
            and not (xyi[1] == self.height - 1 and xyi[2] == 0),
            1,
            self.walls,
        )
        self.walls = self.walls[wall_filter]

    def in_same_set(self, cell1, cell2):
        """
        Checks if two cells are in the same set in self.cells.
        """
        return any([cell1 in cell_set and cell2 in cell_set for cell_set in self.cells])

    def sets_to_merge(self, cell1, cell2):
        """
        Gives the a list containing the positions of the two sets containing cells
        in question.
        """
        return [cell1 in cell_set or cell2 in cell_set for cell_set in self.cells]

    def step(self):
        """
        Runs one step of Kruskal's algorithm.
        """
        dir_key = [[0, +1], [+1, 0]]
        random_index = random.randrange(len(self.walls))
        wall = self.walls[random_index].tolist()
        position = wall[:2]
        position_adjacent = [a + b for a, b in zip(position, dir_key[wall[2]])]

        if (
            position_adjacent[0] > self.width - 1
            or position_adjacent[1] > self.height - 1
        ):
            return 0
        is_wall = lambda x: not all([a == b for a, b in zip(wall, x)])
        wall_filter = np.apply_along_axis(is_wall, 1, self.walls)
        self.walls = self.walls[wall_filter]
        if self.in_same_set(position, position_adjacent):
            return 0
        self.wall_map[wall[0], wall[1], wall[2]] = False
        remove = self.sets_to_merge(position, position_adjacent)
        keep = [not elt for elt in remove]
        self.cells = list(it.compress(self.cells, keep)) + [
            list(it.chain.from_iterable(it.compress(self.cells, remove)))
        ]

    def remove_wall(self, wall):
        """
        Removes a wall from the wall_map.
        """
        self.wall_map[wall[0], wall[1], wall[2]] = False

    def add_start(self, cell, exterior_wall):
        """
        Adds a start label and removes an exterior wall.
        """
        self.start = cell
        self.remove_wall(exterior_wall)

    def add_end(self, cell, exterior_wall):
        """
        Adds a end label and removes an exterior wall.
        """
        self.end = cell
        self.remove_wall(exterior_wall)

    def complete(self):
        """
        Runs Kruskal's algorithm until the maze is complete.
        """
        while len(self.cells) > 1:
            self.step()
