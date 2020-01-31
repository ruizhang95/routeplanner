import numpy as np
from numpy.linalg import norm

class heuristic2D(object):
    """ compute heuristic score """
    
    def __init__(self, step=10, diagonal=14):
        """
        Attributes:
        self.STEP: integer/float (default: 10)
            cost of moving to adjacent grid. (four directions)
        self.DIAG: integer/float (default: 14)
            cost of moving diagonally to adjacent grid. (eight directions)
        """
        self.STEP = step
        self.DIAG = diagonal 

    def adaptWeight(self, u, v, order='mean'):
        """ compute adaptive/expected weight of each step between u & v
        Params:
        u, v: tuples of coordinates
        order: str (default: 'mean')
            methods to calculate the weight, including 'mean', 'gaussian'
        Returns:
        adaweight: a float number representing the adaptive weight
        """

        raise NotImplementedError('not implemented')
            
    def null(self, u, v):
        """ not to use heuristic"""
        return 0
    
    def manhattan(self, u, v):
        """ manhattan heuristic
        Params:
        u, v: tuples of coordinates        
        Returns: 
        distance: float
        """
        delta = np.array(u)-np.array(v)
        distance = self.STEP*norm(delta, ord=1)
        return distance
    
    def chebyshev(self, u, v):
        """ chebyshev heuristic
        Params:
        u, v: tuples of coordinates
        """
        delta = np.array(u)-np.array(v)
        distance = self.STEP*norm(delta, ord=np.inf)
        return distance
    
    def octile(self, u, v):
        """ octile heuristic
        Params:
        u, v: tuples of coordinates
        """
        delta = np.abs(np.array(u)-np.array(v))
        distance = self.STEP*np.amax(delta) + (self.DIAG - self.STEP)*np.amin(delta)
        return distance
    
    def euclidean(self, u, v):
        """ manhattan heuristic
        Params:
        u, v: tuples of coordinates
        """
        delta = np.array(u)-np.array(v)
        distance = self.STEP*norm(delta, ord=None)
        return distance
    
if __name__=='__main__':
    h = heuristic2D()
    u = (0,0)
    v = (3,4)
    print(h.manhattan(u, v))
    print(h.chebyshev(u, v))
    print(h.octile(u, v))
    print(h.euclidean(u, v))
