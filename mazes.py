import numpy as np

class SquareMaze:
    dir_names = np.array(["East", "South", "West", "North"], dtype=(np.unicode_, 5))
    dir_offsets = np.array([[+1, 0], [0, +1], [-1, 0], [0, -1]], dtype=(np.int32))
    wall_key = np. array([[0, 0, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 1]], dtype=(np.int32))
    
    def __init__(self, walls):
        self.walls = walls
        self.walls[0,:,0] = False
        self.walls[:,0,1] = False
        self.width, self.height, self.half_num_sides = walls.shape
