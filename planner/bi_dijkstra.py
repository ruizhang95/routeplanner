from multiprocessing import Pool

from planner.routeplanner import RoutePlanner as rp

class BiDijkstra(rp):
    def __init__(self, heuristic='manhattan', alpha=2):
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


    def _relax(self, u, v, table, to_target=True):
        """Perform edge relaxation. 
        Params:
        u: a tuple representing the coordinates of the node u
        v: a tuple representing the coordinates of the node v
        table: a nested default dictionary {(coordinate): {'g':, 'f':, 'parent':}}
        to_target: bool (default: True)
            if True, the corresponding lookup table should be self.nodes and it 
            relaxes nodes from source to target; otherwise, corresponding table 
            should be self.nodes_inv and it relaxes nodes from target to source.
        """
        # g_val is the tentative actual distance from node v to source node via u.
        g_val = table[u]['g'] + self.graph[u][v]['weight']
               
        # Relax node v from node u.
        if g_val < table[v]['g']:
            
            # If to_target is True, h_val is the heuristic (a guess value) of distance 
            # from v to target. Otherwise, h_val is the heuristic from v to source.
            if to_target:
                h_val = self.h(v, self.target)
            else:
                h_val = self.h(v, self.source)
            
            # f_val is the combined score of both distances.
            # f_val is slightly different from the textbook version by a alpha factor.
            f_val = self.alpha*g_val + (2-self.alpha)*h_val            
            
            # update lookup table
            table[v]['g'] = g_val
            table[v]['f'] = f_val
            table[v]['parent'] = u
            
            # if node is unvisited or is closed but can be accessed in a cheaper way,
            # add it to open priority queue.
            if to_target and (v not in self.open):
                self.open.add(v, f_val)
                # if node v reopens, it should be remove from the close set
                if v in self.close:
                    self.close.remove(v)
            if not to_target and (v not in self.open_inv):
                self.open_inv.add(v, f_val)
                # if node v reopens, it should be removed from the close_inv set
                if v in self.close_inv:
                    self.close_inv.remove(v)
    
    def plan(self, source, target, graph=None):
        """Find path from a single source with Dijkstra's algorithm
        dijkstra is the only method capable for one-to-many search in this library
        Params:
        graph: a networkx graph object
        source: a tuple representing the coordinates of the source node
        target: a tuple representing the coordinates of the target node
        Returns:

        """
        if graph is not None:
            self.graph = graph
        if self.graph is None:
            raise ValueError('graph is not initialized')
        self.source = source
        self.target = target

        # check source and target in graph for early stop.
        if self.source not in self.graph:
            raise ValueError('Invalid source. Source not in the graph')
        if self.target not in self.graph:
            raise ValueError('Invalid target. Target not in the graph')
        
        # initialize both source and target
        self._init(bi_direct=True)
        
        self._callHeuristic(step=1.0, diag=1.4)
        
        while self.open.cnt > 0 and self.open_inv.cnt > 0:
            node = self.open.pop()
            node_inv = self.open_inv.pop()
            self.close.add(node)
            self.close_inv.add(node_inv)
            #print('open: ', node, end='\t')
            #print('open_inv: ', node_inv, end='\n')
            if node in self.close_inv:
                path, weight = self._findPath(node, self.nodes)
                path_inv, weight_inv = self._findPath(node, self.nodes_inv)

                return (path[:-1]+path_inv[::-1], weight+weight_inv)
            if node_inv in self.close:
                path, weight = self._findPath(node_inv, self.nodes)
                path_inv, weight_inv = self._findPath(node_inv, self.nodes_inv)
                return (path[:-1]+path_inv[::-1], weight+weight_inv)
                
            # relax from source
            for neighbor in self.graph.adj[node]:
                self._relax(node, neighbor, self.nodes, True)
            # relax from target
            for neighbor in self.graph.adj[node_inv]:
                self._relax(node_inv, neighbor, self.nodes_inv, False)
        # if no such path exists return None
        return ([],None)      

    def multi_plan(self, pairs, graph):
        """ Process multiple pairs of source-target in one map
        Params:
        pair: list of tuple in the form of [(source_1, target_1),(source_2, target_2)...]
        Returns:
        map: a dictionary in the form of {(source, target): (path, weight)}
        """
        self.graph = graph
        res = []
        for pair in pairs:
            res.append(self.plan(pair[0], pair[1]))
        return res
