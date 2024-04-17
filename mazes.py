import numpy as np
import matplotlib.pyplot as plt

class SquareMaze:
    dir_names = np.array(["East", "South", "West", "North"], dtype=(np.unicode_, 5))
    dir_offsets = np.array([[+1, 0], [0, +1], [-1, 0], [0, -1]], dtype=(np.int32))
    wall_key = np. array([[0, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 1]], dtype=(np.int32))
    
    def __init__(self, walls):
        self.walls = walls
        self.walls[0,:,0] = False
        self.walls[:,0,1] = False
        self.width, self.height, self.half_num_sides = walls.shape

    def draw_horizontal(self):
        is_wall = self.walls[:,:,0]
        is_not_wall = np.logical_not(is_wall)
        xs = np.broadcast_to(np.arange(self.width), (self.height, self.width)).transpose()
        ys = np.broadcast_to(np.arange(self.height), (self.width, self.height))
        plt.hlines(ys[is_wall], xs[is_wall]-1, xs[is_wall], color="black")
        plt.hlines(ys[is_not_wall], xs[is_not_wall]-1, xs[is_not_wall], color="lightgray", linestyle="dashed")

    def draw_vertical(self):
        is_wall = self.walls[:,:,1]
        is_not_wall = np.logical_not(is_wall)
        xs = np.broadcast_to(np.arange(self.width), (self.height, self.width)).transpose()
        ys = np.broadcast_to(np.arange(self.height), (self.width, self.height))
        plt.vlines(xs[is_wall], ys[is_wall]-1, ys[is_wall], color="black")
        plt.vlines(xs[is_not_wall], ys[is_not_wall]-1, ys[is_not_wall], color="lightgray", linestyle="dashed")

    def draw(self, name):
        self.draw_horizontal()
        self.draw_vertical()
        plt.xticks([])
        plt.yticks([])
        plt.xlim([-1-0.01,self.width-1])
        plt.ylim([-1-0.01,self.height-1])
        plt.ylim(max(plt.ylim()), min(plt.ylim()))
        plt.gca().set_aspect('equal')
        plt.savefig(name)
        