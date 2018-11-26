import collections


Border = collections.namedtuple('Boundary', ['x1', 'y1', 'x2', 'y2'])


class Block:
    def __init__(self, graph, boundary,  IMSIZE):
        self.boundary = boundary
        self.tree = graph.do_QBT(self.boundary, IMSIZE)

    def get_subtree(self, leaf_name):
        return self.tree.subtree(leaf_name)
