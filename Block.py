class Block:
    def __init__(self, graph, IMSIZE):
        self.tree = graph.do_QBT(IMSIZE)

    def get_subtree(self, leaf_name):
        return self.tree.subtree(leaf_name)
