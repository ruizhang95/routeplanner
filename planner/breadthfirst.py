import numpy as np
import networkx as nx

from planner.dijkstra import Dijkstra
from utils.heuristic import heuristic2D


class BreadthFirst(Dijkstra):
    def __init__(self, heuristic='octile', alpha=2):
        """
        Params:
        heuristic: {'manhattan', 'chebyshev', 'octile','euclidean','null'} (default: 'manhattan')
            methods to compute heuristic.
        alpha: a number in range of [0, 2] (default: 1)
            if alpha is 0, it becomes best first search; if alpha is 1, it is A*;
            if alpha is 2, it becomes dijkstra algorithm.
            Warning: be really careful to select alpha, because it trades off between
            accuracy and speed.
        """
        super().__init__(heuristic=heuristic, alpha=alpha)
        
    def _relax(self, u, v):
        """Perform edge relaxation. 
        Params:
        u: a tuple representing the coordinates of the node u
        v: a tuple representing the coordinates of the node v

        """
        
        # g_val is the tentative actual distance from node v to source node via u.
        g_val = self.nodes[u]['g'] + self.h(u, v)
        # Relax node v from node u.
        # update g_val 
        if g_val < self.nodes[v]['g']:
            f_val = g_val        
            
            self.nodes[v]['g'] = g_val
            self.nodes[v]['f'] = f_val
            self.nodes[v]['parent'] = u
            
            # if node is unvisited or is closed but can be accessed in a cheaper way,
            # add to open priority queue.
            if v not in self.open:
                self.open.add(v, f_val)
