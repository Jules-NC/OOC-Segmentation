from Tree import *
from Image import *


def generate_leafs(boundary, IMSIZE):
    return [Node(name=int_refchange(i, IMSIZE, boundary), altitude=0) for i in index(boundary)]


def index(bound):
    img_len = boundary_to_image_size(bound)
    for i in range(img_len.len_x * img_len.len_y):
        yield i


def do_QBT(graph, IMSIZE):
    graph.sort()
    nodes = generate_leafs(graph.boundary, IMSIZE)
    # [refchange(nodes[i], IMSIZE, graph.boundary) for i in range(len(nodes))]

    for i, edge in enumerate(graph):
        e1 = int_refchange(edge[0], IMSIZE, graph.boundary)
        e2 = int_refchange(edge[1], IMSIZE, graph.boundary)

        # print(edge[0], edge[1])
        # print(e1, e2)
        # print()
        if (nodes[edge[0]].root() is nodes[edge[1]].root()):
            continue

        nodes.append(Node(name=(e1, e2),
                          altitude=graph.weights[i],
                          childs=(nodes[edge[0]].root(), nodes[edge[1]].root())))
        nodes[edge[0]].root().parent = nodes[-1]
        nodes[edge[1]].root().parent = nodes[-1]
    # print("--------------------")
    res = Tree(nodes)
    return res

def refchange(node, IMSIZE, boundary):
    x1, y1 = coords_change(int(node.name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    node.name = y1 * IMSIZE.len_x + x1


def int_refchange(int_name, IMSIZE, boundary):
    x1, y1 = coords_change(int(int_name), boundary_to_image_size(boundary))
    x1 += boundary.x1
    y1 += boundary.y1
    return y1 * IMSIZE.len_x + x1


def coords_change(i, imsize):
    y = i // imsize.len_y
    x = i % imsize.len_x
    return (x, y)


def merge(nodes1, nodes2, edge):
    pass
