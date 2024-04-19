import numpy as np
import matplotlib.pyplot as plt
import random
import itertools as it


class SquareMaze:
    half_num_sides = 2

    def __init__(self, wall_map):
        self.wall_map = wall_map
        self.cut_out_of_bounds()
        self.width, self.height, x = self.wall_map.shape
        if self.half_num_sides != x:
            print("ERROR: wall_map shape incorrect")

    def cut_out_of_bounds(self):
        self.wall_map[0, :, 0] = False
        self.wall_map[:, 0, 1] = False

    def plot(self):
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

        plt.xticks([])
        plt.yticks([])
        plt.xlim([-0.01, self.width - 1])
        plt.ylim([-0.01, self.height - 1])
        plt.ylim(max(plt.ylim()), min(plt.ylim()))
        plt.gca().set_aspect("equal")
        return plt


class SquareKruskalMaze(SquareMaze):
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
        wall_filter = np.apply_along_axis(
            lambda xyi: not (xyi[0] == 0 and xyi[2] == 1)
            and not (xyi[1] == 0 and xyi[2] == 0)
            and not (xyi[0] == self.width - 1 and xyi[2] == 1)
            and not (xyi[1] == self.height - 1 and xyi[2] == 0),
            1,
            self.walls,
        )
        self.walls = self.walls[wall_filter]

    def in_same_set(self, pair1, pair2):
        return any([pair1 in cell_set and pair2 in cell_set for cell_set in self.cells])

    def sets_to_merge(self, pair1, pair2):
        return [pair1 in cell_set or pair2 in cell_set for cell_set in self.cells]

    def step(self):
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

    def complete(self):
        while len(self.cells) > 1:
            self.step()
