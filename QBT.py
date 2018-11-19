from Tree import *
from Image import *


def generate_leafs(boundary, IMSIZE):
    return [Node(name=int_coords_ibloc_to_iimage(i, IMSIZE, boundary), altitude=0) for i in index(boundary)]


def index(bound):
    img_len = boundary_to_image_size(bound)
    for i in range(img_len.len_x * img_len.len_y):
        yield i


def do_QBT(graph, IMSIZE):
    graph.sort()
    nodes = generate_leafs(graph.boundary, IMSIZE)

    for i, edge in enumerate(graph):
        e1 = int_coords_ibloc_to_iimage(edge[0], IMSIZE, graph.boundary)
        e2 = int_coords_ibloc_to_iimage(edge[1], IMSIZE, graph.boundary)

        if nodes[edge[0]].root() is nodes[edge[1]].root():
            continue

        nodes.append(Node(name=(e1, e2),
                          altitude=graph.weights[i],
                          childs=(nodes[edge[0]].root(), nodes[edge[1]].root())))
        nodes[edge[0]].root().parent = nodes[-1]
        nodes[edge[1]].root().parent = nodes[-1]
    res = Tree(nodes)
    return res


def coords_ibloc_to_iimage(node, IMSIZE, boundary):
    x1, y1 = coords_i_to_xy(int(node.name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    node.name = y1 * IMSIZE.len_x + x1


def int_coords_ibloc_to_iimage(int_name, IMSIZE, boundary):
    x1, y1 = coords_i_to_xy(int(int_name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    return y1 * IMSIZE.len_x + x1


def coords_i_to_xy(i, imsize):
    """
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


def merge(nodes1, nodes2, edge):
    pass
