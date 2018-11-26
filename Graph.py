import numpy as np


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
        self.im_size = boundary_to_image_size(self.boundary)

        # Nombre de vertices compaptible avec le boundary
        a = boundary_to_image_size(self.boundary)
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

    def do_QBT(self, IMSIZE):
        self.sort()
        nodes = generate_leafs(self.boundary, IMSIZE)

        for i, edge in enumerate(self):
            e1 = int_coords_ibloc_to_iimage(edge[0], IMSIZE, self.boundary)
            e2 = int_coords_ibloc_to_iimage(edge[1], IMSIZE, self.boundary)

            if nodes[edge[0]].root() is nodes[edge[1]].root():
                continue

            nodes.append(Node(name=(e1, e2),
                              altitude=self.weights[i],
                              childs=(nodes[edge[0]].root(), nodes[edge[1]].root())))
            nodes[edge[0]].root().parent = nodes[-1]
            nodes[edge[1]].root().parent = nodes[-1]
        res = Tree(nodes)
        return res


from Tree import *
from Image import *


def generate_leafs(boundary, IMSIZE):
    """
    IS = b = ImageSize(4,2)
    b = Boundary(0,0,1,1)

    generate_leafs(b, IS) will return:
        0
        1
        3
        4
    """
    return [Node(name=int_coords_ibloc_to_iimage(i, IMSIZE, boundary), altitude=0) for i in index(boundary)]


def index(bound):
    """
    Used in addition to generate_leafs when i are required to name nodes
    index(Boundary(0,0,1,1)) will yield:
        0
        1
        2
        3
    and so on, it
    """
    img_len = boundary_to_image_size(bound)
    for i in range(img_len.len_x * img_len.len_y):
        yield i



def coords_ibloc_to_iimage(node, IMSIZE, boundary):
    """
    Require the IMSIZE and the boundary
    Convert i0', i1', ... to i0, i1, ...

    i' represent the index in the boundary
    i' is the name of the node
    i represent the index of a node in the image

    return i
    """
    x1, y1 = coords_i_to_xy(int(node.name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    node.name = y1 * IMSIZE.len_x + x1


def int_coords_ibloc_to_iimage(int_name, IMSIZE, boundary):
    """
    Require the IMSIZE and the boundary
    Convert i0', i1', ... to i0, i1, ...

    i' is the index of int_name in the boundary
    i' is int_name
    i represent the index of a node in the image

    return i
    """
    x1, y1 = coords_i_to_xy(int(int_name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    return y1 * IMSIZE.len_x + x1


def coords_i_to_xy(i, imsize):
    """
    Require the IMSIZE and the boundary
    Referential change from i0, i1, i2, ... to (x0, y0), (y2, y2), ...

    0123 => | 0 : (x=0, y=0) | 4 : (x=0, y=1)
    4567 => | 1 : (x=1, y=0) |

    >>> print(coords_i_to_xy(2, ImageSize(2,2)))
    (0, 1)
    >>> print(coords_i_to_xy(2, ImageSize(2,4)))
    (0, 1)
    >>> print(coords_i_to_xy(0, ImageSize(1,1)))
    (0, 0)
    """
    x = i % imsize.len_x
    y = i // imsize.len_x

    return (x, y)


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
