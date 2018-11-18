import numpy as np
from Image import *

class Graph:
    def __init__(self, boundary, n_vertices=0, edges=[], weights=[]):
        """
        A Graph is the sum of:
            - a list of Edges
            - one weight per edge
            - a boundary

        :param n_vertices: Number of vertices in the new graph.  # TODO: regarder si c'est vraiment utile
        :param edges: List of the edges of the graph
        :param weights: List of the weights of the edges. weight[0] corresponds to the weight of edges[0]
        :param boundary: Where this graph is located ?
        """
        assert len(edges) == len(weights), "Incompatible length"

        self.edges = list(edges)
        self.weights = weights
        self.it_size = len(edges)
        self.n_vertices = n_vertices  # nbr of vertices
        self.boundary = boundary
        self.im_size = bound_to_imglen(self.boundary)

        # Nombre de vertices compaptible avec le boundary
        a = bound_to_imglen(self.boundary)
        assert a.len_x * a.len_y == n_vertices, "Incompatible boundaries"

        # Sort directly after being created to not do this in the main code, because we don't want to modify a Graph.
        self.sort()

    def sort(self):
        self.weights, self.edges = zip(*sorted(zip(self.weights, self.edges)))

    def __iter__(self):
        for edge in self.edges:
            yield edge

    def __len__(self):
        return self.it_size

    def __str__(self):
        res = ""
        for edge, weight in zip(self.edges, self.weights):
            res += str(edge) + " : " + str(weight) + "\n"
        return res


def generate_graph(imsize):
    X = imsize.len_x
    Y = imsize.len_y

    edges = []
    for y in range(Y):
        for x in range(X):
            pos = x + y * X
            eq1 = x + 1 + y * X
            if x + 1 < X:
                edges.append((pos, eq1))
            eq2 = x + (y + 1) * X
            if y + 1 < Y:
                edges.append((pos, eq2))
    weights = [abs(int(i)) for i in np.random.normal(110, 40, len(edges))]

    graph1 = Graph(n_vertices=X * Y, edges=edges, weights=weights, boundary=Boundary(0, 0, X - 1, Y - 1))
    return graph1
