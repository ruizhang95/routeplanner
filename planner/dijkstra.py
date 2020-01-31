from planner.routeplanner import RoutePlanner as rp
from multiprocessing import Pool

class Dijkstra(rp):
    def __init__(self, heuristic='null', alpha=2):
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

    def plan(self, source, target, graph=None):
        """Find path from a single source with Dijkstra's algorithm
        dijkstra is the only method capable for one-to-many search in this library
        Params:
        graph: a networkx graph object
        source: a tuple representing the coordinates of the source node
        target: a tuple representing the coordinates of the target node
        Returns:
        (path, weight): a tuple 
            path is a list of nodes in the shortest path from source to target, and 
            weight is an integer/float number denoting the cumulative weights of the path.
            For an unaccessible target return [] as path and None as weight.
            e.g. ([(2, 0), (1, 0), (0, 1), (1, 2), (2, 2)], 4.8),
            ([], None), ([(2, 0), (2, 0)], 0)
        """
        if graph is not None:
            self.graph = graph
        if self.graph is None:
            raise ValueError('graph is not initialized')
        self.source = source
        self.target = target
        
        # check source and target
        if self.source not in self.graph:
            raise ValueError('Invalid source. Source not in the graph')
        if self.target not in self.graph:
                raise ValueError('Invalid target. Target not in the graph')
        
        # initialize single source
        self._init()
        self._callHeuristic(step=1.0, diag=1.4)
        
        while self.open.cnt > 0:
            node = self.open.pop()
            if node == self.target:
                path, weight = self._findPath(node, self.nodes)
                return (path, weight)
            # relaxation
            for neighbor in self.graph.adj[node]:
                self._relax(node, neighbor)
        
        # if no such path exists return None
        return ([], None)

    def multi_plan(self, pairs, graph):
        """ Process multiple source-target pairs in one map
        Params:
        pair: list of tuple in the form of [(source_1, target_1),(source_2, target_2)...]
        Returns:
        map: a dictionary in the form of {(source, target): (path, weight)}
        """
        self.graph=graph
        res = []
        for pair in pairs:
            res.append(self.plan(pair[0], pair[1]))
        return res
