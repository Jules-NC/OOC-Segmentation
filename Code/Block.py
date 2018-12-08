from Code.Node import *
from Code.Tree import *
from Code.GraphPrinter import *


class Block:

    def __init__(self, graph, border):
        self.border = border
        self.tree = graph.do_QBT(self.border)

    def update_tree(self, new_subtree, leaf):
        # search the leaf
        # compare
        selector_new = new_subtree.find_leaf(leaf)
        new_list = self.tree.nodes
        selector_down = self.tree.find_leaf(leaf)
        selector_up = selector_down

        while selector_new is not None:
            while selector_up == selector_new and selector_up is not None:
                selector_new = selector_new.parent
                selector_down = selector_up
                # new_list.append(selector_down)
                selector_up = selector_up.parent
            if selector_new is not None:
                selector_down.unbind_parent()
                selector_down.bind_parent(Node(name=selector_new.name, parent=selector_up,
                                               altitude=selector_new.altitude))
                selector_down = selector_down.parent
                new_list.append(selector_down)
                selector_new = selector_new.parent

        new_list.sort()
        self.tree = Tree(new_list)

    def get_subtree(self, leaf_name):
        return self.tree.subtree(leaf_name)
