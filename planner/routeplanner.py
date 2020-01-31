import math
from collections import defaultdict as dd

import numpy as np
import networkx as nx

from utils.priorq import priorq
from utils.heuristic import heuristic2D

class RoutePlanner(object):
    def __init__(self, heuristic='manhattan', alpha=1):
        """
        Params:
        heuristic: {'manhattan', 'chebyshev', 'octile','euclidean','null'} (default: 'manhattan')
            methods to compute heuristic.
        alpha: a number in range of [0, 2] (default: 1)
            if alpha is 0, it becomes best first search; if alpha is 1, it is A*;
            if alpha is 2, it becomes dijkstra algorithm.
            Warning: be really careful to select alpha, because it trades off between
            accuracy and speed.
        
        Attributes:
        graph: a networkx graph object
        source: a tuple representing the coordinates of the source node
        target: a tuple or a list of tuple representing the coordinates of the target node
        MAX: a constant representing the weight of an unwalkable edge
        """
        self.heuristic = heuristic
        self.alpha = alpha
        self.graph = None
        self.source = None
        self.target = None
        self.MAX = math.inf
        
    def _callHeuristic(self, step=10, diag=14):
        """ function to initialize specific heuristic"""
        h = heuristic2D(step, diag)
        name2func = {'manhattan': h.manhattan,
                    'chebyshev': h.chebyshev,
                    'octile': h.octile,
                    'euclidean': h.euclidean,
                    'null': h.null}
        self.h = name2func[self.heuristic]
            
    def _init(self, bi_direct=False):
        """Initialize single source"""
        # initialize a nested dictionary with default values of g_val, f_val and parent
        self.nodes = dd(lambda: {'g': self.MAX, 'f': self.MAX, 'parent': None})
        # initialize a priority queue of nodes to be checked aka. frontiers/ open list
        self.open = priorq() 
        # initialize source node
        self.open.add(self.source, 0)
        
        self.nodes[self.source]['g'] = 0
        
        # if bi_direct is True, initialize both source and target
        if bi_direct:
            
            # initialize lookup table and open list
            self.nodes_inv = dd(lambda: {'g': self.MAX, 'f': self.MAX, 'parent': None})
            self.open_inv = priorq()
            
            # initialize target node
            self.open_inv.add(self.target, 0)
            self.nodes_inv[self.target]['g'] = 0

            # initialize sets of checked nodes.
            self.close = set()
            self.close_inv = set()
            
    def _relax(self, u, v):
        """Perform edge relaxation. 
        Params:
        u: a tuple representing the coordinates of the node u
        v: a tuple representing the coordinates of the node v
        """
        # g_val is the tentative actual distance from node v to source node via u.
        g_val = self.nodes[u]['g'] + self.graph[u][v]['weight']
               
        # Relax node v from node u.
        if g_val < self.nodes[v]['g']:
            
            # h_val is the heuristic (a guess value) of distance from v to target
            h_val = self.h(v, self.target)

            # f_val is the combined score of both distances.
            # f_val is slightly different from the textbook version by a alpha factor.
            f_val = self.alpha*g_val + (2-self.alpha)*h_val            
            
            # update node status lookup table
            self.nodes[v]['g'] = g_val
            self.nodes[v]['f'] = f_val
            self.nodes[v]['parent'] = u
            
            # if node is unvisited or is closed but can be accessed in a cheaper way,
            # add to the open priority queue.
            if v not in self.open:
                self.open.add(v, f_val)
                    

    def _findPath(self, node, table):
        """Find path from the lookup table
        Params:
        node: a tuple representing the coordinates of the node
        table: a lookup table (either self.nodes or self.nodes_inv)
        Returns:
        path: a list of nodes in the shortest path from start to node.
        weight: a integer/floating number denoting the cumulative weights of the shortest path.
        """
        
        current = node
        parent = table[current]['parent']      
        path = [current]
        while parent != None:
            path.append(parent)
            current = parent
            parent = table[current]['parent']
        return (path[::-1], table[node]['g'])

