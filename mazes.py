import numpy as np
import matplotlib.pyplot as plt

class SquareMaze:
    dir_names = np.array(["East", "South", "West", "North"], dtype=(np.unicode_, 5))
    dir_offsets = np.array([[+1, 0], [0, +1], [-1, 0], [0, -1]], dtype=(np.int32))
    wall_key = np. array([[0, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 1]], dtype=(np.int32))

    
    def __init__(self, is_wall_map):
        self.is_wall = is_wall_map
        self.is_wall[0,:,0] = False
        self.is_wall[:,0,1] = False
        self.width, self.height, self.half_num_sides = self.is_wall.shape
        self.xs = np.broadcast_to(np.arange(self.width), (self.height, self.width)).transpose()
        self.ys = np.broadcast_to(np.arange(self.height), (self.width, self.height))

    def draw_horizontal(self):
        is_not_wall = np.logical_not(self.is_wall[:,:,0])
        plt.hlines(self.ys[self.is_wall[:,:,0]], self.xs[self.is_wall[:,:,0]]-1, self.xs[self.is_wall[:,:,0]], color="black")
        plt.hlines(self.ys[is_not_wall], self.xs[is_not_wall]-1, self.xs[is_not_wall], color="lightgray", linestyle="dashed")

    def draw_vertical(self):
        is_not_wall = np.logical_not(self.is_wall[:,:,1])
        plt.vlines(self.xs[self.is_wall[:,:,1]], self.ys[self.is_wall[:,:,1]]-1, self.ys[self.is_wall[:,:,1]], color="black")
        plt.vlines(self.xs[is_not_wall], self.ys[is_not_wall]-1, self.ys[is_not_wall], color="lightgray", linestyle="dashed")

    def plot(self):
        self.draw_horizontal()
        self.draw_vertical()
        plt.xticks([])
        plt.yticks([])
        plt.xlim([-0.01,self.width-1])
        plt.ylim([-0.01,self.height-1])
        plt.ylim(max(plt.ylim()), min(plt.ylim()))
        plt.gca().set_aspect('equal')
        return plt
