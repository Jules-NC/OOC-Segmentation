from Code.Node import *
from Code.Tree import *
from Code.GraphPrinter import *

class Block:

    def __init__(self, graph, border, index):
        self.border = border
        self.index = index
        self.tree = graph.do_QBT(self.border)

    def update_tree(self, new_subtree, leaves):
        new_list = self.tree.nodes
        for leaf in leaves:
            # search the leaf
            # selector_new goes up the new subtree as selector down and up work together at the original one
            selector_new = new_subtree.find_leaf(leaf)
            selector_down = self.tree.find_leaf(leaf)
            selector_up = selector_down

            # while we did not reach the root
            while selector_new is not None:
                # while they are reaching the same node the selectors go up the tree
                while selector_up == selector_new and selector_up is not None:
                    selector_new = selector_new.parent
                    # selector down has to always be the new child and selector up the new parent
                    selector_down = selector_up
                    selector_up = selector_up.parent

                if selector_new is not None:
                    # unbind the selector_down's parent so that a new node with the characteristics of new node can
                    # become it's new parent
                    selector_down.unbind_parent()
                    # create a new node while binding it as a child of the selector_up and becoming parent of
                    # selector_down
                    selector_down.bind_parent(Node(name=selector_new.name, parent=selector_up,
                                                   altitude=selector_new.altitude))
                    # selector down now becomes the new node and its values are appendend on the new nodes list
                    selector_down = selector_down.parent
                    new_list.append(selector_down)
                    # update selector new
                    selector_new = selector_new.parent

        new_list.sort()
        self.tree = Tree(new_list)
        print_tree(self.tree, "Block_"+str(self.index))

    def get_subtree(self, leaves_name):
        return self.tree.leaves_subtree(leaves_name)

    def get_border_tree(self, list_border):
        return self.tree.leaves_subtree(list_border)