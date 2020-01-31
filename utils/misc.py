import itertools
import math

import networkx as nx
import numpy as np
import cv2

# Recipe from the itertools documentation.
def pairwise(iterable, cyclic=False):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    first = next(b, None)
    if cyclic is True:
        return zip(a, itertools.chain(b, (first,)))
    return zip(a, b)


# grid constructor via array
def arr2grid(array, diagonal=False, weight=1, create_using=None):
    """Returns the cooresponding grid graph of the image.
    The grid graph has each node connected to its four nearest neighbors or
    eight nearest neighbors if diagonal is True.
    Params
    -------
    array: list or numpy array representing the binarized input image, value of 
        each pixel should be either 0 or 1, where 1 is walkable(white), 0 is block.
        1 is the default weight for each step.
    diagonal: bool (default: False)
        If this is 'True' the nodes are connected to its eight nearest neighbors.
    weight: array-like or an integer(default: 1)
        array should be in the same size as the input array. use the same weight matrix
        in the heuristics in order to have same scale.
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
    Returns
    -------
    NetworkX graph
    """

    data = np.array(array)
    # keep the walkable area with default weight 1, or use the given weight.
    weight = np.where(data==0, 0, weight)
    
    # initialize an empty networkx graph
    G = nx.empty_graph(0, create_using)
    m, n = data.shape
    rows = range(m)
    cols = range(n)
    
    # compute the weight between two adjacent grids by averaging their weight value.
    traffic = lambda a, b: (weight[a]+weight[b])/2
    
    # add nodes from the input array
    G.add_nodes_from((i, j) for i in rows for j in cols)
    
    # add edges for the four directions connection
    G.add_edges_from(((i, j), (pi, j), {'weight': traffic((i, j), (pi, j))})
                     for pi, i in pairwise(rows) for j in cols)
    G.add_edges_from(((i, j), (i, pj), {'weight': traffic((i, j), (i, pj))})
                     for i in rows for pj, j in pairwise(cols))
    
    # add edges for the diagonal connections in eight directions.
    if diagonal is True:
        G.add_edges_from(((i, j), (pi, pj), {'weight': 1.414*traffic((i, j), (pi, pj))})
                     for pi, i in pairwise(rows) for pj, j in pairwise(cols))
        G.add_edges_from(((pi, j), (i, pj), {'weight': 1.414*traffic((pi, j), (i, pj))})
                     for pi, i in pairwise(rows) for pj, j in pairwise(cols))
    
    # remove the unwalkable nodes and edges
    unwalkable = [tuple(n) for n in np.argwhere(data==0)]
    G.remove_nodes_from(unwalkable)
    
    # both directions for directed
    if G.is_directed():
        G.add_edges_from((v, u) for u, v in G.edges())
    return G

# grid constructor via image
def img2grid(img_path, diagonal=False, weight=None, create_using=None):
    # load image and convert color space into grayscale
    im_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # binarize
    # set walkable area as 255, unwalkable as 0.
    _, im_bw = cv2.threshold(im_gray, 254, 255, cv2.THRESH_BINARY)
    # normalize pixel value
    data = im_bw/255
    return arr2grid(data, diagonal, weight, create_using)

if __name__ == '__main__':

    # test grid generator
    array = np.array([[1,1,1],[0,0,0],[1,0,1]])
    grid = arr2grid(array)
    print(grid.nodes)
    print(grid.edges)
    print(grid[(0,0)])
    try:
        print(grid[(1,1)])
    except:
        print("node not in grid")