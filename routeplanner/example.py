import numpy as np
from utils.misc import arr2grid
from planner.astar import AStar
from planner.dijkstra import Dijkstra
from planner.bestfirst import BestFirst
from planner.breadthfirst import BreadthFirst
from planner.bi_astar import BiAStar
from planner.bi_dijkstra import BiDijkstra
from planner.bi_bestfirst import BiBestFirst

# e.g [[1, 0, 1],
#      [1, 0, 1],
#      [1, 1, 1]]
img = np.array([[1,1,1],[1,0,1],[1,0,1]])
# convert array to networkx graph
grid = arr2grid(img, diagonal=True)
source = (2,0)
target = (2,2)
#target = [(1,1),(2,2),(2,1)]
rp = BiAStar()
route = rp.multi_plan([((2,0), (2,2)), ((2,0), (0,0))], graph=grid)
#route = rp.plan(source, target, grid)
print(route)