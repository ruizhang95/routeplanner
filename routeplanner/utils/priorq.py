import heapq
import itertools

class priorq(object):
    def __init__(self):
        self.pq = []
        self.cnt = 0
        # mapping node to entry
        self.entryFinder = {}
        self.counter = itertools.count()
        self.REMOVED = '<removed-node>'
        
    def __contains__(self, value):
        """membership tests using in. O(1)"""
        return value in self.entryFinder
        
    def add(self, node, priority, tieBreaker=None):
        """Add a new node or update the priority(distance) of an existing node. O(logn)
        Params:
        node: any object
        priority: integer/float
            representing the priority of current node
        tieBreaker: a comparable object
            a value for breaking tie
        """
        self.cnt += 1
        if node in self.entryFinder:
            self.remove(node)
        if tieBreaker is None:
             tieBreaker = next(self.counter)
        entry = [priority, tieBreaker, node]
        self.entryFinder[node] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, node):
        """Mark an existing node as REMOVED. O(1).Raise KeyError if not found."""
        entry = self.entryFinder.pop(node)
        entry[-1] = self.REMOVED
        self.cnt -= 1

    def pop(self):
        """Remove and return the lowest priority task. O(logn) Raise KeyError if empty."""
        while self.pq:
            _, _, node = heapq.heappop(self.pq)
            if node is not self.REMOVED:
                del self.entryFinder[node]
                self.cnt -= 1
                return node
        raise KeyError('pop from an empty priority queue')
        
    def __str__(self):
        return str(self.pq)
    
    



if __name__ == '__main__':
    # test priority queue
    pq = priorq()
    pq.add_node((1,1),4)
    pq.add_node((1,2),2)
    pq.remove_node((1,2))
    print(pq)
    print(pq.pop_node())
    print(pq)
    pq.add_node((1,3),1)
    pq.add_node((1,3),4)
    print(pq)
