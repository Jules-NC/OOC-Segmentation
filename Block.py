from QBT import *


class Block:
    def __init__(self, graph, IMSIZE):
        self.tree = do_QBT(graph, IMSIZE)

    def get_subtree(self, leaf_name):
        return self.tree.subtree(leaf_name)
