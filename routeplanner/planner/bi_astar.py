from planner.bi_dijkstra import BiDijkstra

class BiAStar(BiDijkstra):
    def __init__(self, heuristic='manhattan', weight=None, alpha=1):
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

