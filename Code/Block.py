

class Block:
    def __init__(self, graph, border):
        self.border = border
        self.tree = graph.do_QBT(self.border)

    def get_subtree(self, leaf_name):
        return self.tree.subtree(leaf_name)

    def update_tree(self, new_subtree):
        # search the leaf
        # compare
        current_node_boundary = new_subtree.nodes[0]
        current_node_blocktree = self.tree.nodes[0]

        if current_node_blocktree == current_node_boundary:
            current_node_blocktree = current_node_blocktree.

