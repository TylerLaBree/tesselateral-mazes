# Tesselateral Mazes

Generate mazes out of any equilateral which tessellates the plane.

## Getting Started

Start by running `chmod +x make-venv.sh` and then `./make-venv.sh`. You'll only need to
do this on first setup, or each time you update to a new version which includes a new
virtual environment.

On a fresh terminal, run `source activate-venv.sh` to setup python packages. If you
want a jupyter lab session, run `jupyter lab`, and select the `localhost` link.

## Generate a Kruskal Square Maze

Here's some sample code to generate a 10 by 10 square-tiling maze using Kruskal's Algorithm. You can also provide a seed, so you get the same maze each time. In this case, the seed is 10.

```
from mazes import SquareKruskalMaze

my_maze = SquareKruskalMaze(10, 10, seed=10)
my_maze.complete()
my_maze.add_start([1, 0], [1, 0, 0])
my_maze.add_end([11, 10], [10, 10, 1])
my_maze.plot().show()
```

This should generate a maze which looks like the following

![kruskal-10x10](https://github.com/TylerLaBree/tesselateral-mazes/assets/51167014/6f445eb0-b907-47d0-8c6b-cecf054816f5)
