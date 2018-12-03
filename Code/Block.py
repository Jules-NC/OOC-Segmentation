

class Block:
    def __init__(self, graph, border):
        self.border = border
        self.tree = graph.do_QBT(self.border)

    def get_subtree(self, leaf_name):
        return self.tree.subtree(leaf_name)
    def updateTree(self, newBoundary, leaf_index):
        # search the leaf
        # compare
        pass