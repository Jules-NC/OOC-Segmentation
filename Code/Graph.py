import numpy as np
from Code.Tree import *
from Code.Border import *


class Graph:
    def __init__(self, n_vertices=0, edges=None, weights=None):
        """
        A Graph is the sum of:
            - a list of Edges
            - one weight per edge
            - a border

        :param n_vertices: Number of vertices in the new graph.
        :param n_vertices:
        :param edges: List of the edges of the graph
        :param weights: List of the weights of the edges. weight[0] corresponds to the weight of edges[0]
        """
        assert len(edges) == len(weights), "Incompatible length"

        self.edges = list(edges)
        self.weights = weights
        self.it_size = len(edges)
        self.n_vertices = n_vertices  # nbr of vertices

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

    def do_QBT(self, border):
        self.sort()
        nodes = border.generate_leafs()

        for i, edge in enumerate(self):
            e1 = int_coords_ibloc_to_iimage(edge[0], border)
            e2 = int_coords_ibloc_to_iimage(edge[1], border)

            if nodes[edge[0]].root() is nodes[edge[1]].root():
                continue

            nodes.append(Node(name=(e1, e2),
                              altitude=self.weights[i],
                              left=nodes[edge[0]].root(),
                              right=nodes[edge[1]].root()))
        res = Tree(nodes)
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

    graph1 = Graph(n_vertices=X * Y, edges=edges, weights=weights)
    return graph1
